# Text cleaning function

textcleanFunc <- function (corp) {
  corp <- tm_map(corp, stripWhitespace)
  corp <- tm_map(corp, PlainTextDocument)
  corp <- tm_map(corp, removePunctuation)
  corp <- tm_map(corp, removeNumbers)
  corp <- tm_map(corp, removeWords, c(stopwords("german"), stopwords("SMART"),
                                      stopwords("french"), "the", "a"))
  corp <- tm_map(corp, stemDocument)
}

# Part of speech tagging function
# http://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html


AdjExtract <- function (s){ # take a character string and extract adjectives
  a2 <- annotate(s, list(Maxent_Sent_Token_Annotator(),Maxent_Word_Token_Annotator()))
  a3 <- annotate(s, Maxent_POS_Tag_Annotator(), a2)
  
  # extracts tags associated with each word
  a3w <- subset(a3, type == "word" )
  tags <- sapply(a3w$features, `[[`, "POS")
  
  ## Extract adjectives & nouns
  adjIndex <- which(tags=="JJ" | tags=="JJR" | tags=="JJS" | tags=="NN"  | tags=="NNS"  | tags=="NNP" | tags=="NNPS" )
  paste(s[a3w][adjIndex], collapse = ' ')
}


# Wordcloud gen function

CCClouds <- function(dataframe, reviewVar, categVar, subsetVal) {
  u <- dataframe[dataframe[categVar] == subsetVal,reviewVar]
  u <- u[sapply( u, function(x) length(x)>0)] # drop empty reviews
  u <- gsub("  ","", paste(u, collapse=' '))
  
  if (nchar(u)==1) d="Error, no reviews found." else {
    u <- AdjExtract(as.String(u)) # replace with just adjectives & nouns
    
    tmCorpus <- Corpus(VectorSource(u))
    
    tmText <- textcleanFunc(tmCorpus)
    
    term.matrix <- TermDocumentMatrix(tmText)
    
    m <- as.matrix(term.matrix)
    v <- sort(rowSums(m),decreasing=TRUE)
    d <- data.frame(word = names(v),freq=v)
  }  
    return (d)
}

wordcloudBy1Dist <- function(name) {
  d <- CCClouds(dataframe=MainDF, reviewVar="AllReviews", categVar="District", 
                subsetVal=name)
  
  wordcloud(d$word,d$freq, max.words=25, 
            random.order=F, rot.per=.15, 
            colors=brewer.pal(9, "OrRd")[-(1:3)])
  
  text(x=.5, y=1., labels=name,col="black",cex=1.5)
}