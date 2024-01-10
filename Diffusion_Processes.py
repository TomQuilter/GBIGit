import torch
import math

#Two ***IMAGES***  of size 32x32 PIXELS with 3 channels - RGB
x0 = torch.randn(2,3,32,32)

print(x0)

Betas = torch.tensor([0.05, 0.1, 0.15, 0.2, 0.25])

t= torch.tensor([1, 3])    ### Position of images?!

# Betas are the amount of noise to be added at each time step
# Alphas are the amount of noise to be subtracts at each time step

alphas = 1 - Betas

print("alphas: ", alphas)

alpha_hat = torch.cumprod(alphas, axis=0)

print("alpha_hat: ", alpha_hat)

print( alpha_hat.size())

###############################
## CREATE THE 1st and 3rd Noisy Images
###############################

# Grab the  1st and 3rd numbers needed from alpha_hat
result = alpha_hat.gather(-1,t).reshape(-1,1,1,1)
 
print("result: ", result)

print(result.size())

print(x0.size())

mean = result.sqrt()*x0
print("mean: ", mean)

noise = torch.randn_like(x0)
print("noise: ", noise)
variance = torch.sqrt(1-result*noise)
print("variance: ", variance)
