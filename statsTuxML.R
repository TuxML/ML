library(ggplot2)
library(readr)
library(rpart)
library(rpart.plot)
library(randomForest)
library(caret)
library(gbm)
library(dplyr)
library(randomForestExplainer)

# TODO we assume that a res.csv exists (typically a CSV extracted from the database)
res <- read.csv("/Users/macher1/Documents/SANDBOX/csvTuxml/ProjetIrma/csvgen/res3.csv") 

res$KERNEL_SIZE <- res$KERNEL_SIZE / 1048576
# res <- subset(res, KERNEL_SIZE != 0)
# res <- res[20:nrow(res),]

print(paste("configuration options", ncol(res)))
print(paste("number of configs", nrow(res))) 

myes <- apply(res, MARGIN = 1, FUN = function(x) length(x[x == "m"]))
smyes <- summary(myes)
print(paste("average number of m", smyes['Mean'])) 
print(paste("min number of m", min(myes))) 
print(paste("max number of m", max(myes))) 

nyes <- apply(res, MARGIN = 1, FUN = function(x) length(x[x == "y"]))
syes <- summary(nyes)
print(paste("average number of yes", syes['Mean'])) 
print(paste("min number of yes", min(nyes))) 
print(paste("max number of yes", max(nyes))) 

nyesAndM <- apply(res, MARGIN = 1, FUN = function(x) length(x[x == "y" | x == "m"]))
syesAndM <- summary(nyesAndM)
print(paste("average number of yes/m", syesAndM['Mean'])) 
print(paste("min number of yes/m", min(nyesAndM))) 
print(paste("max number of yes/m", max(nyesAndM))) 



# res$nbActiveOptions <- nyes

comptime <- res$COMPILE_TIME

ksize <- res$KERNEL_SIZE 
#print("Kernel sizes in Mo")
#print(ksize)

print("Kernel size (in Mo)")
print(summary(ksize))

print("Compilation time")
print(summary(comptime))

print(paste("correlation between size and compilation time", cor(ksize, comptime)))

print(paste("correlation between active options (yes and m) and comp time ", cor(nyesAndM, comptime)))
print(paste("correlation between active options (yes and m) and kernel size ", cor(nyesAndM, ksize)))

print(paste("correlation between yes options and comp time ", cor(nyes, comptime)))
print(paste("correlation between yes options and kernel size ", cor(nyes, ksize)))

print(paste("correlation between m options and comp time ", cor(myes, comptime)))
print(paste("correlation between m options and kernel size ", cor(myes, ksize)))

# Bar plot
bp<- ggplot(res, aes(x=CONFIG_DEBUG_INFO, y=""))+
  geom_bar(width = 1, stat = "identity")
bp

#counts = table(res$CONFIG_UBSAN_SANITIZE_ALL)  ## get counts
#labs = paste(res$CONFIG_UBSAN_SANITIZE_ALL, counts)  ## create labels
#pie(counts, labels = labs)  ## plot




N_TRAINING = 1000

# splitdf function will return a list of training and testing sets
splitdf <- function(dataframe, seed=NULL) {
  if (!is.null(seed)) set.seed(seed)
  index <- 1:nrow(dataframe)
  #trainindex <- sample(index, trunc(length(index)/2))
  trainindex <- sample(index, trunc(N_TRAINING))
  trainset <- dataframe[trainindex, ]
  testset <- dataframe[-trainindex, ]
  list(trainset=trainset,testset=testset)
}

NTREE = 1000

mkRandomForest <- function(dat) {
  # mtry <- (ncol(dat) - 7) # 7: because we excluse non predictor variables! => BAGGING (m=p)
  return (randomForest (KERNEL_SIZE~CONFIG_SFC_FALCON+CONFIG_SENSORS_LTC4245+CONFIG_DEBUG_INFO_REDUCED+CONFIG_KEYBOARD_DLINK_DIR685+CONFIG_DEBUG_INFO_SPLIT+CONFIG_SENSORS_TMP103
                        +CONFIG_SND_OSSEMUL+CONFIG_SOUND_OSS_CORE+                                    
                          CONFIG_SCSI_FUTURE_DOMAIN+CONFIG_NET_VENDOR_NVIDIA+CONFIG_MEGARAID_LEGACY+CONFIG_UBSAN_SANITIZE_ALL                                 
                        +CONFIG_DEBUG_INFO+CONFIG_GDB_SCRIPTS+CONFIG_ROCKETPORT+CONFIG_HID_SENSOR_HUMIDITY+CONFIG_REGULATOR_LP873X+CONFIG_ACPI_CMPC
                        +CONFIG_MODULES+CONFIG_STRICT_MODULE_RWX+CONFIG_RANDOMIZE_BASE+CONFIG_X86_NEED_RELOCS+CONFIG_SCSI_CXGB3_ISCSI+CONFIG_RTLWIFI
                        , data=dat,importance=TRUE,ntree=NTREE,keep.forest=TRUE,na.action=na.exclude))
}

mkBoosting <- function(dat) {
  return(
    gbm(KERNEL_SIZE~.-COMPILE_TIME, 
        data=dat,distribution="gaussian",n.tree=100)
  )
}

plotFtImportance <- function(rtree) {
  
  impPlot <- rtree$variable.importance %>%
    data_frame(variable = names(.), importance = .) %>%
    mutate(importance = importance / sum(importance)) %>%
    top_n(20) %>%
    ggplot(aes(x = importance,
               y = reorder(variable, importance))) +
    geom_point() +
    labs(title = "Importance of configuration options ",
         subtitle = "(20 most relevant scaled to sum 1)") +
    theme_bw() +
    theme(axis.title.y = element_blank(),
          plot.title = element_text(hjust = 0.5),
          plot.subtitle = element_text(hjust = 0.5),
          axis.line = element_line(colour = "grey"),
          panel.grid.major = element_blank(), panel.border = element_blank()) +
    geom_segment(aes(x = -Inf, y = reorder(variable, importance),
                     xend = importance, yend = reorder(variable, importance)),
                 size = 0.2)
  
  print(impPlot)
}

predComputation <- function(iris) {
  
  #apply the function
  splits <- splitdf(iris)
  
  # save the training and testing sets as data frames
  training <- splits$trainset
  testing <- splits$testset
  
  rtree <- # mkBoosting(training)
    #mkRandomForest(training)
    # KERNEL_SIZE~CONFIG_SFC_FALCON+CONFIG_SENSORS_LTC4245+CONFIG_DEBUG_INFO_REDUCED+CONFIG_KEYBOARD_DLINK_DIR685+CONFIG_DEBUG_INFO_SPLIT+CONFIG_SENSORS_TMP103
    #       +CONFIG_SND_OSSEMUL+CONFIG_SOUND_OSS_CORE+                                    
    #       CONFIG_SCSI_FUTURE_DOMAIN+CONFIG_NET_VENDOR_NVIDIA+CONFIG_MEGARAID_LEGACY+CONFIG_UBSAN_SANITIZE_ALL                                 
    #       +CONFIG_DEBUG_INFO+CONFIG_GDB_SCRIPTS+CONFIG_ROCKETPORT+CONFIG_HID_SENSOR_HUMIDITY+CONFIG_REGULATOR_LP873X+CONFIG_ACPI_CMPC
    #       +CONFIG_MODULES+CONFIG_STRICT_MODULE_RWX+CONFIG_RANDOMIZE_BASE+CONFIG_X86_NEED_RELOCS+CONFIG_SCSI_CXGB3_ISCSI+CONFIG_RTLWIFI
    #     
    # KERNEL_SIZE~.-COMPILE_TIME
    rpart(KERNEL_SIZE~.-COMPILE_TIME, data=training,
      method = "anova",
      parms = list(split = "information"),
       control = rpart.control(minsplit = 2,
                               minbucket = 8,
      #                         #maxdepth = maxDepth,
      #                         #cp = complexity,
                               usesurrogate = 0,
                               maxsurrogate = 0)
     )

  rpart.plot(rtree)
  plotFtImportance(rtree)
  # imp <- varImp(rtree)
  #varImpPlot(rtree)
  #plot(rtree)
  #print(plot_min_depth_distribution(rtree))
  #print(plot_multi_way_importance(rtree, size_measure = "no_of_nodes"))
  # print(plot_min_depth_interactions(rtree))
  # print (rownames(imp)[order(imp$Overall, decreasing=TRUE)])
  
  # cp <- as_tibble(rtree$cptable) %>%
  #   filter(xerror <= min(xerror) + xstd) %>%
  #   filter(xerror == max(xerror)) %>%
  #   select(CP) %>%
  #   unlist()
  # 
  # rtree <- prune(rtree, cp = cp)
  # rpart.plot(rtree)
  # plotFtImportance(rtree)
  # print(rtree)
  #print(varImp(rtree))
  #print(varImp(rtree))
  
  
  # print(rtree$variable.importance)
  
  # plot(imp, top=20)
  
 
  #print(sort(varImp(rtree), decreasing = TRUE))
  # what are the important variables (via permutation)
  
  
  #predict the outcome of the testing data
  predicted <- predict(rtree, newdata=testing)
  #predicted <- predict(model, data=testing) # for CART 

  # what is the proportion variation explained in the outcome of the testing data?
  # i.e., what is 1-(SSerror/SStotal)
  actual <- testing$KERNEL_SIZE 
  rsq <- 1-sum((actual-predicted)^2)/sum((actual-mean(actual))^2)
  #rsq <- sum((actual-predicted)^2)/sum((actual-mean(actual))^2)
  list(act=actual,prd=predicted,rs=rsq)
}

predKernelSizes <- predComputation(res)
predKernelSizes$d <- abs((predKernelSizes$act - predKernelSizes$prd) / predKernelSizes$act) 
mae <- ((100 / length(predKernelSizes$d)) * sum(predKernelSizes$d))
print(paste("MAE", mae))
