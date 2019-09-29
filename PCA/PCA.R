rm(list = ls())
args = commandArgs(trailingOnly = TRUE)

##setwd(args[1])
library(ggfortify)
library(Rtsne)
############################## P C A ############################## 

            ################### pca_a #################

# Choose the data file
inputData <- read.delim(paste(gsub("\\\\","/",args[1]),"/pca_a.txt",sep = ""), header = FALSE)

# Extract the numeric data into a separate data frame
inputNumericData <- inputData[,1:ncol(inputData)-1]

# Extract the names of the Diseases in a seperate list
inputLabels <- as.data.frame((rev(inputData)[1]))
colnames(inputLabels) <- c("Labels")


# Normalise the data
scaledData <-  as.data.frame(scale(inputNumericData, center = TRUE, scale = FALSE))

# Find the covariance matrix
covMatrix <- cov(scaledData)

# Find the eigen vectors and eigen values
eigenDecomp <- eigen(covMatrix)

# Extract the first 2 loadings of Eigen Vectors
vectorLoadings <- eigenDecomp$vectors[,1:2]
vectorLoadings <- -vectorLoadings

# Calculate the Pricipal Component Scores
PC1 <- as.matrix(inputNumericData) %*% vectorLoadings[,1]
PC2 <- as.matrix(inputNumericData) %*% vectorLoadings[,2]

PC <- data.frame(Diseases = inputLabels, PC1, PC2)

# Plot Principal Components for each State
x11()
p<-ggplot(PC,aes(x=PC1,y=PC2,color=Labels ))
p<-p+ggtitle("PCA plot:pca_a")+geom_point()
p
            ###########################################
            ################### pca_b #################

# Choose the data file
inputData <- read.delim((paste(gsub("\\\\","/",args[1]),"/pca_b.txt",sep = "")), header = FALSE)

# Extract the numeric data into a separate data frame
inputNumericData <- inputData[,1:ncol(inputData)-1]

# Extract the names of the Diseases in a seperate list
inputLabels <- as.data.frame((rev(inputData)[1]))
colnames(inputLabels) <- c("Labels")


# Normalise the data
scaledData <-  as.data.frame(scale(inputNumericData, center = TRUE, scale = FALSE))

# Find the covariance matrix
covMatrix <- cov(scaledData)

# Find the eigen vectors and eigen values
eigenDecomp <- eigen(covMatrix)

# Extract the first 2 loadings of Eigen Vectors
vectorLoadings <- eigenDecomp$vectors[,1:2]
vectorLoadings <- -vectorLoadings

# Calculate the Pricipal Component Scores
PC1 <- as.matrix(inputNumericData) %*% vectorLoadings[,1]
PC2 <- as.matrix(inputNumericData) %*% vectorLoadings[,2]

PC <- data.frame(Diseases = inputLabels, PC1, PC2)

# Plot Principal Components for each State
x11()
p<-ggplot(PC,aes(x=PC1,y=PC2,color=Labels ))
p<-p+ggtitle("PCA plot:pca_b")+geom_point()
p
            ###########################################
            ################### pca_c #################

# Choose the data file
inputData <- read.delim((paste(gsub("\\\\","/",args[1]),"/pca_c.txt",sep = "")), header = FALSE)

# Extract the numeric data into a separate data frame
inputNumericData <- inputData[,1:ncol(inputData)-1]

# Extract the names of the Diseases in a seperate list
inputLabels <- as.data.frame((rev(inputData)[1]))
colnames(inputLabels) <- c("Labels")

# Normalise the data
scaledData <-  as.data.frame(scale(inputNumericData, center = TRUE, scale = FALSE))

# Find the covariance matrix
covMatrix <- cov(scaledData)

# Find the eigen vectors and eigen values
eigenDecomp <- eigen(covMatrix)

# Extract the first 2 loadings of Eigen Vectors
vectorLoadings <- eigenDecomp$vectors[,1:2]
vectorLoadings <- -vectorLoadings
PC1 <- as.matrix(inputNumericData) %*% vectorLoadings[,1]
PC2 <- as.matrix(inputNumericData) %*% vectorLoadings[,2]

PC <- data.frame(Diseases = inputLabels, PC1, PC2)

# Plot Principal Components for each State
x11()
p<-ggplot(PC,aes(x=PC1,y=PC2,color=Labels ))
p<-p+ggtitle("PCA plot:pca_c")+geom_point()
p

################################################################### 
############################## S V D ############################## 

            ################### pca_a #################

# Choose the data file
inputData <- read.delim((paste(gsub("\\\\","/",args[1]),"/pca_a.txt",sep = "")), header = FALSE)

# Extract the numeric data into a separate data frame
inputNumericData <- inputData[,1:ncol(inputData)-1]

# Extract the names of the Diseases in a seperate list
inputLabels <- as.data.frame((rev(inputData)[1]))
colnames(inputLabels) <- c("Labels")

# Perform SVD
svdResult <- svd(inputNumericData)

# Extract the u orthogonal matrix
svdResult.u <- as.data.frame(svdResult$u)

# Components to plot
Component1 <- as.matrix(svdResult.u$V1)
Component2 <- as.matrix(svdResult.u$V2)
PC <- data.frame(Diseases = inputLabels, Component1, Component2)

x11()
# Plot the graph
p<-ggplot(PC,aes(x=Component1,y=Component2,color=Labels ))
p<-p+ggtitle("SVD plot:pca_a")+geom_point()
p

            ###########################################
            ################### pca_b #################

# Choose the data file
inputData <- read.delim((paste(gsub("\\\\","/",args[1]),"/pca_b.txt",sep = "")), header = FALSE)

# Extract the numeric data into a separate data frame
inputNumericData <- inputData[,1:ncol(inputData)-1]

# Extract the names of the Diseases in a seperate list
inputLabels <- as.data.frame((rev(inputData)[1]))
colnames(inputLabels) <- c("Labels")

# Perform SVD
svdResult <- svd(inputNumericData)
c
# Extract the u orthogonal matrix
svdResult.u <- as.data.frame(svdResult$u)

# Components to plot
Component1 <- as.matrix(svdResult.u$V1)
Component2 <- as.matrix(svdResult.u$V2)
PC <- data.frame(Diseases = inputLabels, Component1, Component2)

x11()
# Plot the graph
p<-ggplot(PC,aes(x=Component1,y=Component2,color=Labels ))
p<-p+ggtitle("SVD plot:pca_b")+geom_point()
p

            ###########################################
            ################### pca_c #################

# Choose the data file
inputData <- read.delim((paste(gsub("\\\\","/",args[1]),"/pca_c.txt",sep = "")), header = FALSE)

# Extract the numeric data into a separate data frame
inputNumericData <- inputData[,1:ncol(inputData)-1]

# Extract the names of the Diseases in a seperate list
inputLabels <- as.data.frame((rev(inputData)[1]))
colnames(inputLabels) <- c("Labels")


# Perform SVD
svdResult <- svd(inputNumericData)

# Extract the u orthogonal matrix
svdResult.u <- as.data.frame(svdResult$u)

# Components to plot
Component1 <- as.matrix(svdResult.u$V1)
Component2 <- as.matrix(svdResult.u$V2)
PC <- data.frame(Diseases = inputLabels, Component1, Component2)

x11()
# Plot the graph
p<-ggplot(PC,aes(x=Component1,y=Component2,color=Labels ))
p<-p+ggtitle("SVD plot:pca_c")+geom_point()
p

################################################################### 
############################## t - S N E ##########################

            ################### pca_a #################

# Choose the data file
inputData <- read.delim((paste(gsub("\\\\","/",args[1]),"/pca_a.txt",sep = "")), header = FALSE)

# Extract the numeric data into a separate data frame
inputNumericData <- inputData[,1:ncol(inputData)-1]

# Extract the names of the Diseases in a seperate list
inputLabels <- as.data.frame((rev(inputData)[1]))
colnames(inputLabels) <- c("Labels")

# Perform t-SNE
tsne <- Rtsne(inputNumericData[,-1], dims = 2, perplexity=30,
              verbose=TRUE, max_iter = 1000, check_duplicates = FALSE)

tsne.Y <- as.data.frame(tsne$Y)

# Components to plot
Component1 <- as.matrix(tsne.Y$V1)
Component2 <- as.matrix(tsne.Y$V2)
PC <- data.frame(Diseases = inputLabels, Component1, Component2)

x11()
# Plot the graph
p<-ggplot(PC,aes(x=Component1,y=Component2,color=Labels ))
p<-p+ggtitle("t-SNE plot:pca_a")+geom_point()
p

            ###########################################
            ################### pca_b #################

# Choose the data file
inputData <- read.delim((paste(gsub("\\\\","/",args[1]),"/pca_b.txt",sep = "")), header = FALSE)

# Extract the numeric data into a separate data frame
inputNumericData <- inputData[,1:ncol(inputData)-1]

# Extract the names of the Diseases in a seperate list
inputLabels <- as.data.frame((rev(inputData)[1]))
colnames(inputLabels) <- c("Labels")

# Perform t-SNE
tsne <- Rtsne(inputNumericData[,-1], dims = 2, perplexity=30,
              verbose=TRUE, max_iter = 1000, check_duplicates = FALSE)

tsne.Y <- as.data.frame(tsne$Y)

# Components to plot
Component1 <- as.matrix(tsne.Y$V1)
Component2 <- as.matrix(tsne.Y$V2)
PC <- data.frame(Diseases = inputLabels, Component1, Component2)

x11()
# Plot the graph
p<-ggplot(PC,aes(x=Component1,y=Component2,color=Labels ))
p<-p+ggtitle("t-SNE plot:pca_b")+geom_point()
p

            ###########################################
            ################### pca_c #################

# Choose the data file
inputData <- read.delim((paste(gsub("\\\\","/",args[1]),"/pca_c.txt",sep = "")), header = FALSE)

# Extract the numeric data into a separate data frame
inputNumericData <- inputData[,1:ncol(inputData)-1]

# Extract the names of the Diseases in a seperate list
inputLabels <- as.data.frame((rev(inputData)[1]))
colnames(inputLabels) <- c("Labels")


# Perform t-SNE
tsne <- Rtsne(inputNumericData[,-1], dims = 2, perplexity=30,
              verbose=TRUE, max_iter = 1000, check_duplicates = FALSE)

tsne.Y <- as.data.frame(tsne$Y)

# Components to plot
Component1 <- as.matrix(tsne.Y$V1)
Component2 <- as.matrix(tsne.Y$V2)
PC <- data.frame(Diseases = inputLabels, Component1, Component2)

x11()
# Plot the graph
p<-ggplot(PC,aes(x=Component1,y=Component2,color=Labels ))
p<-p+ggtitle("t-SNE plot:pca_c")+geom_point()
p


################################################################### 

Sys.sleep(100000)