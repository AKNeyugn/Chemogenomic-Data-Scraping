test <- read.csv("C:\\Users\\anhkh\\Documents\\UBC\\COOP\\S2019 CARDONA LAB\\Wildenhain-Data-Scraper\\CGM\\Spectrum_ED_CGM.csv",sep=",")
mydata <- test[,-1]
rownames(mydata) <- test[,1]
mydata <- na.omit(mydata)
mydata <- scale(mydata)

# Determine number of clusters
wss <- (nrow(mydata)-1)*sum(apply(mydata,2,var))
for (i in 2:12) wss[i] <- sum(kmeans(mydata, 
   centers=i)$withinss)
plot(1:12, wss, type="b", xlab="Number of Clusters",
  ylab="Within groups sum of squares")

# K-Means Cluster Analysis
fit <- kmeans(mydata, 3) # 3 cluster solution
# get cluster means 
aggregate(mydata,by=list(fit$cluster),FUN=mean)
# append cluster assignment
mydata <- data.frame(mydata, fit$cluster)

mydata <- mydata[order(fit$cluster),]
data_matrix <- data.matrix(mydata)
color = rev(heat.colors(256))
heatmap <- heatmap(data_matrix, Rowv=NA, Colv=NA, col = color, scale="column", margins=c(3,3)) 

write(fit[["cluster"]], "~/UBC/COOP/S2019 CARDONA LAB/Wildenhain-Data-Scraper/output.txt")

# Ward Hierarchical Clustering
#d <- dist(mydata, method = "euclidean") # distance matrix
#fit_hclust <- hclust(d, method="ward.D") 
#plot(fit_hclust) # display dendogram
#groups <- cutree(fit_hclust, k=3) # cut tree into 3 clusters
# draw dendogram with red borders around the 3 clusters 
#rect.hclust(fit_hclust, k=3, border="red")