###################################################
# cjgb, 20120710
# lectura de los ficheros de la epa
# hay que bajarlos de http://www.ine.es/prodyser/micro_epa.htm  (de 1T 2005 en adelante)
# se colocan en un directorio en el que est?n solos y descomprimidos
###################################################

setwd('epa-raw')
library(MicroDatosEs)

leer.epa <- function( fichero ){

  dat <- epa2005(fichero)
  dat <- subset( dat, select = c(
    ciclo,
    edad,
    sexo,
    nforma,
    prov,
    aoi,
    factorel) )

  dat$aoi <-  memisc::recode(dat$aoi,
                                "o" = 1 <- 3:4,
                                "p" = 2 <- 5:6,
                                "i" = 3 <- 7:9
                            )

  dat$nforma <- memisc::recode(dat$nforma,
                                "o"  = 1 <- c("AN", "P1"),
                                "p"  = 2 <- "P2",
                                "fp" = 3 <- "SP",
                                "b"  = 4 <- c("S1", "SG"),
                                "u"  = 5 <- "SU")

  tmp <- as.data.frame(dat)

  tmp$edad <- as.numeric( dat$edad )
  tmp$prov <- as.numeric( dat$prov )
  tmp$sexo <- as.numeric( dat$sexo )

  tmp <- tmp[ tmp$edad > 15, ]
  tmp <- tmp[ tmp$aoi != "i", ]
  # tmp <- tmp[ ! ( is.na(tmp$aoi) | tmp$aoi == "i"), ]

  tmp$factorel <- tmp$factorel / 100

  tmp
}

res <- sapply( dir(), leer.epa, simplify = F )
todos <- do.call( rbind, res )
rownames(todos) <- NULL

final <- todos

final <- aggregate(final$factorel, by = subset( final, select = -factorel), sum)
names(final)[ names(final) == "x" ] <- "factorel"


# col.names = F (False)
write.table( final, file = "../datos_epa.csv", row.names = F, col.names = F, sep = "\t", quote = FALSE )
