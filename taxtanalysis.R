setwd("/Users/lubagloukhov/PycharmProjects/scrapely01")


library("openNLP") # req'd for Maxent_Sent_Token_Annotator...
library("NLP") # req'd for annotate...
library("tm") # req'd for Corpus...
library("wordcloud") # req'd for Corpus...


source("dataImportClean.R")
source("intermedFuncs.R")

##################################
# EXPLORATORY
##################################

# By Region

names(MainDF)
summary(MainDF$District)

# Select only those 9 Districts which have >75 observations
names <- names(summary(MainDF$District)[summary(MainDF$District)>75])[-1]
par(mfrow=c(3,3),mar=c(2,2,2,2), oma=c(3,1,0,0))

# Create 9 side by side plots of wordclouds for each District
# OR Dump plots to individual pages in a pdf (uncomment pdf(), dev.off())
# pdf(file='byDist_plot.pdf')
name <- names[1]
for (name in names[1:9]) {
  d <- CCClouds(dataframe=MainDF, reviewVar="AllReviews", categVar="District", 
                subsetVal=name)
  
  wordcloud(d$word,d$freq, max.words=25, 
            random.order=F, rot.per=.15, 
            colors=brewer.pal(9, "OrRd")[-(1:3)])
  
  text(x=.5, y=1., labels=name,col="black",cex=1.5)
}
# dev.off()


# By distillery
summary(MainDF$Distillery)
par(mfrow=c(1,2),mar=c(2,2,2,2), oma=c(3,1,0,0))
plot.new()

for (name in c("Lagavulin")) {
  d <- CCClouds(dataframe=MainDF, reviewVar="AllReviews", categVar="Distillery", 
                subsetVal=name)
  if (class(d)=="character") {
    text(x = 0.5, y = 0.5, "Error, no reviews found.", 
         cex = 1.6, col = "red")
  } else {
    wordcloud(d$word,d$freq, max.words=25, 
              random.order=F, rot.per=.15, 
              colors=brewer.pal(9, "OrRd")[-(1:3)])
    
    text(x=.6, y=1., labels=name,col="black",cex=1.5)
  }
 
}


# BY casktype


for (name in c("Sherry Cask", "Bourbon Cask")) {
  d <- CCClouds(dataframe=MainDF, reviewVar="AllReviews", categVar="Casktype", 
                subsetVal=name)
  
  wordcloud(d$word,d$freq, max.words=25, 
            random.order=F, rot.per=.15, 
            colors=brewer.pal(9, "OrRd")[-(1:3)])
  
  text(x=.5, y=1., labels=name,col="black",cex=1.5)
}


# By age


summary(MainDF$AgeCat)

CCClouds(dataframe=MainDF, reviewVar="AllReviews", categVar="AgeCat", 
         subsetCV=c("Aged", "New"))


# By Rating

MainDF$RatingCat <- as.factor(MainDF$RatingCat)


summary(MainDF$RatingCat)

CCClouds(dataframe=MainDF, reviewVar="AllReviews", categVar="RatingCat", 
         subsetCV=c("Poor", "Exceptional"))



# BY CTAEGORY

summary(MainDF$Category)

CCClouds(dataframe=MainDF, reviewVar="AllReviews", categVar="Category", 
         subsetCV=c("Single Malt from Japan", "Single Malt from Scotland"))

CCClouds(dataframe=MainDF, reviewVar="AllReviews", categVar="Category", 
         subsetCV=c("Single Malt from Islay, Scotland", 
                    "Single Malt from Highlands, Scotland"))

