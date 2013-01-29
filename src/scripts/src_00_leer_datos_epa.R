###################################################
# cjgb, 20120710
# lectura de los ficheros de la epa
# hay que bajarlos de http://www.ine.es/prodyser/micro_epa.htm  (de 1T 2005 en adelante)
# se colocan en un directorio en el que est?n solos y descomprimidos
###################################################

#Dependencias: hace falta tener instalado en el sistema el paquete gcc-fortran
#También el paquete MicroDatosEs; para instalarlo, ejecutar desde la consola de R:
#install.packages("MicroDatosEs", repos= c("http://R-Forge.R-project.org", getOption("repos")))
#Si falla, se puede instalar from source con el fichero MicroDatosEs.tar.gz. Desde la consola de linux:
#R CMD INSTALL MicroDatosEs_0.04.tar.gz
#Hacen falta más dependencias (aparece un error si no están incluidas); para instalarlas:
#install.packages("memisc", repos=c("http://R-Forge.R-project.org", getOption("repos") )
#install.packages("Hmisc", repos=c("http://R-Forge.R-project.org", getOption("repos") )
#PARA INVOCAR ESTE SCRIPT:
#1. setear bien el working directory
#2. ejecutar R CMD BATCH script.R

# seteamos el working directory, donde estén los ficheros
setwd('/home/yami/kaleidos/piweek/tasa-paro/varia/datos-ine/data-raw')
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

	dat$aoi <-  memisc::recode(dat$aoi, "o" = 1 <- 3:4, "p" = 2 <- 5:6, "i" = 3 <- 7:9)

	dat$nforma <- memisc::recode( dat$nforma,
		"o"  = 1 <- c(80,11),
		"p"  = 2 <- c(12,21,22,23,36),
		"fp" = 3 <- c(31,33,34,41,51),
		"b"  = 4 <- c(32),
		"u"  = 5 <- c(50,52:56,59,61) )

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


# otras manipulaciones

write.table( final, file = "../datos_epa.csv", row.names = F, col.names = T, sep = "\t", quote = FALSE )

# ejemplos de gr?ficos
# para calcular la tasa de paro no hay que contar ocupados  y parados (o y p), sino sumar el factorel para cada grupo y 
# calcular luego el cociente entre todos los activos (o+p) y los parados (p):



'''
tmp <- by( final$factorel, list(final$ciclo, final$aoi, final$nforma), sum )
tp <- tmp[,2, "o"] / (tmp[,2,"o"] + tmp[,1,"o"] )
plot(tp, type = "l", ylim = c(0,0.5) )
tp <- tmp[,2, "u"] / (tmp[,2,"u"] + tmp[,1,"u"] )
lines(tp, col = "red" )
tp <- tmp[,2, "b"] / (tmp[,2,"b"] + tmp[,1,"b"] )
lines(tp, col = "blue" )
tp <- tmp[,2, "fp"] / (tmp[,2,"fp"] + tmp[,1,"fp"] )
lines(tp, col = "green" )




tmp <- by( todos.agr$factorel, list(todos.agr$ciclo, todos.agr$aoi), sum )
tp <- tmp[,2] / (tmp[,1] + tmp[,2])

tmp <- by( todos.agr$factorel, list(todos.agr$ciclo, todos.agr$aoi, todos.agr$nforma), sum )
tp <- tmp[,2, "u"] / (tmp[,2,"u"] + tmp[,1,"u"] )
plot(tp, type = "l" )
'''





