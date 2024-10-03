import sys
from models.vae.vrae import VRAE
import models.gans.doppelganger.dgan as dpgan
import numpy as np
import torch
from collections import defaultdict
import pandas as pd

device = "cuda" if torch.cuda.is_available() else "cpu"


class DataGenerate:
    def __init__(self, m_config):
        self.m_config = m_config

    def gen_timeganpt(self, X_train,y_train):
        columns=X_train.columns
        parameters_=self.m_config["parameters"]
        parameters = {
                'hidden_dim': parameters_["hidden_dim"],
                'num_layer': parameters_["num_layer"],  # Certifique-se de que este valor seja pelo menos 1
                'iterations': parameters_["iterations"],
                'batch_size': parameters_["batch_size"],
                'module': 'lstm'
                    } 
        def extract_time(data):
            time = []
            max_seq_len = 0
            for i in range(len(data)):
                temp_time = len(data[i])
                time.append(temp_time)
                if temp_time > max_seq_len:
                    max_seq_len = temp_time
            return time, max_seq_len

        from models.gans.timeganpt.timegan import TimeGAN

        # Obter o formato de entrada
        reshape = True
        if reshape:
            n_amostras = X_train.shape[0]
            X_train = X_train.values.reshape(n_amostras, 60, 6)
        print("X_train.shape", X_train.shape)
        print("y_train.shape", y_train.shape)
        class_data = defaultdict(list)
        for X, y in zip(X_train, y_train):
            class_data[y].append(X)

        # Gerar dados sintéticos para cada classe
        synthetic_data_by_class = {}
        num_samples_per_class = self.m_config['n_gen_samples']  # Número de amostras sintéticas para gerar por classe
        embeddings_data = []

        for class_label, X_class_data in class_data.items():
            X_class_data = np.array(X_class_data)
            ori_time, _ = extract_time(X_class_data)
            # Criar e treinar o TimeGAN
            timegan = TimeGAN(X_class_data, parameters)
            #timegan.to(device)  # Mover TimeGAN para GPU
            timegan.train()  
            synthetic_data = timegan.generate(num_samples=num_samples_per_class)
            synthetic_data_by_class[class_label] = synthetic_data
    
        synthetic_df = pd.DataFrame()

        
        for class_label, synthetic_data in synthetic_data_by_class.items():
            # Mover o tensor para a CPU se necessário e converter para NumPy
            if isinstance(synthetic_data, torch.Tensor):
                synthetic_data = synthetic_data.cpu().numpy()

            # Reorganizar os dados de (n, 60, 6) para (n, 360)
            synthetic_data = synthetic_data.reshape(synthetic_data.shape[0], -1)  # (-1) automaticamente calcula a dimensão correta
            
            # Criar um DataFrame para os dados sintéticos da classe atual
            class_df = pd.DataFrame(synthetic_data)
            class_df.columns=columns
            # Adicionar uma coluna para a classe
            class_df['label'] = class_label
            
            # Concatenar com o DataFrame geral
            synthetic_df = pd.concat([synthetic_df, class_df], ignore_index=True)
        
        print(synthetic_df.columns)

            
        return synthetic_df

    def train(self, X_train, y_train):
        if self.m_config["name"] == "vrae":
            print("vae")

        elif(self.m_config['name']=='timeganpt'):
           synthetic_df = self.gen_timeganpt(X_train,y_train)

        elif self.m_config["name"] == "Doppelgangerger":
            synthetic_df = dpgan.dgan(self.m_config, X_train, y_train)

        elif self.m_config["name"] == "diffusion_unet1d":
            from models.diffusion.diffusion import DiffusionTrainer
            from models.diffusion.unet.unet_1d import UNet

            params = self.m_config["parameters"]
            model = UNet(in_channel=params["in_channel"],
                         out_channel=params["out_channel"],
                         seq_length=X_train.shape[-1]).to(device)
            diffusion = DiffusionTrainer(model, X_train.shape[-1], X_train.shape[1], epochs=self.m_config['epochs'])
            diffusion.train(X_train)
            synthetic_samples = diffusion.sample(batch_size=self.m_config['n_gen_samples'])
            synthetic_samples = synthetic_samples.view(synthetic_samples.shape[0], -1)
            synthetic_df = pd.DataFrame(synthetic_samples.numpy())
            synthetic_df['label'] = [-1] * self.m_config['n_gen_samples']

        return synthetic_df
