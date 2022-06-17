qx = read.csv('TABUAS.csv', sep = ';', dec = ',')
# SEGURO DE VIDA VITALICIO ------------------------------------------------
A = function(tabua = 'AT_49_F', idade, juros){
  qx = qx[, tabua]
  v = (1+juros)**-1
  qx = qx[(idade+1):length(qx)]
  px = c(1,1-qx[1:(length(qx)-1)])
  t = c(0:(length(qx)-1))
  pxx = cumprod(px)
  return(
    sum(v**(t+1)*pxx*qx)
  )
  
}

# SEGURO DE VIDA VITALICIO DIFERIDO -------------------------------------------------
A_dif = function(tabua = 'AT_49_F', idade, juros, dif){
  qx = qx[, tabua]
  v = (1+juros)**-1
  qx = qx[(idade+1):length(qx)]
  px = c(1,1-qx[1:(length(qx)-1)])
  t = c(0:(length(qx)-1))
  dotal = v**(dif)*prod(px[1:dif])
  pxx = cumprod(px)
  return(
    sum(v**(t+1)*pxx*qx)*dotal
  )
  
}

# SEGURO DE VIDA TEMPORARIO -----------------------------------------------
A_temp = function(tabua = 'AT_49_F', idade, juros, n){
  qx = qx[, tabua]
  v = (1+juros)**-1
  qx = as.numeric(na.exclude(qx[(idade+1):(idade+n)]))
  px = c(1,1-qx[1:(n-1)])
  t = c(0:(n-1))
  pxx = cumprod(px)
  return(
    sum(v**(t+1)*pxx*qx)
  )
  
}

# SEGURO DE VIDA TEMPORARIO E DIFERIDO ------------------------------------
A_temp_dif = function(tabua = 'AT_49_F', idade, juros, n, dif){
  qx = qx[, tabua]
  v = (1+juros)**-1
  qx = as.numeric(na.exclude(qx[(idade+1):(idade+n+dif)]))
  px = c(1,1-qx[1:(n+dif-1)])
  t = c(0:(n-1))
  dotal = v**(dif)*prod(px[1:dif])
  pxx = cumprod(px[(dif+1):(length(px))])
  
  return(
    sum(v**(t+1)*pxx*qx[(dif+1):(dif+n)])*dotal
  )
  
}

# SEGURO DE VIDA DOTAL PURO -----------------------------------------------
A_dotal = function(tabua = 'AT_49_F', idade, juros, n){
  qx = qx[, tabua]
  v = (1+juros)**-1
  qx[is.na(qx)] = 1
  px = 1-qx
  dotal = (v^n)*prod(px[(idade+1):(idade+n)])
  return(dotal)
}

# SEGURO DE VIDA DOTAL MISTO ----------------------------------------------
A_dotal_misto = function(tabua = 'AT_49_F', idade, juros, n){
  puro = A_dotal(tabua = tabua, idade = idade, juros = juros, n = n)
  temp = A_temp(tabua = tabua, idade = idade, juros = juros, n = n)
  return(puro + temp)
}

# ANUIDADE ANTECIPADA VITALICIA  ------------------------------------------------------
a_ant_vit = function(tabua = 'AT_49_F', idade, juros){
  qx = qx[, tabua]
  qx[is.na(qx)] = 1
  px = 1-qx
  pxx = c(1, cumprod(px[(idade+1):length(px)]))
  v = (1+juros)**-1
  t <- (0:(length(pxx)-1))
  return(sum(v^(t)*pxx))
}

# ANUIDADE ANTECIPADA TEMPORARIA ------------------------------------------
a_ant_temp = function(tabua = 'AT_49_F', idade, juros, n){
  qx = qx[, tabua]
  qx[is.na(qx)] = 1
  px = 1-qx
  pxx = c(1, cumprod(px[(idade+1):(idade+n-1)]))
  v = (1+juros)**-1
  t <- (0:(n-1))
  return(sum(v^(t)*pxx))
}

# ANUIDADE ANTECIPADA VITALICIA E DIFERIDA --------------------------------
a_ant_vit_dif = function(tabua = 'AT_49_F', idade, juros, dif){
  qx = qx[, tabua]
  v = (1+juros)**-1
  qx[is.na(qx)] = 1
  px = 1-qx
  dotal = (v^dif)*prod(px[(idade+1):(idade+dif)])
  pxx = c(1, cumprod(px[(idade+dif+1):(length(px)-1)]))
  t = (0:(length(pxx)-1))
  return(dotal*sum(v**t * pxx))
}

# ANUIDADE ANTECIPADA DIFERIDA E TEMPORARIA -------------------------------
a_ant_temp_dif = function(tabua = 'AT_49_F', idade, juros, n, dif){
  qx = qx[, tabua]
  v = (1+juros)**-1
  qx[is.na(qx)] = 1
  px = 1-qx
  dotal = (v^dif)*prod(px[(idade+1):(idade+dif)])
  pxx = c(1, cumprod(px[(idade+dif+1):(idade+dif+n-1)]))
  t = (0:(length(pxx)-1))
  return(dotal*sum(v**t * pxx))
}

# ANUIDADE POSTECIPADA VITALICIA ------------------------------------------
a_post_vit = function(tabua = 'AT_49_F', idade, juros){
  qx = qx[, tabua]
  qx[is.na(qx)] = 1
  px = 1-qx
  pxx = c(cumprod(px[(idade+1):length(px)]))
  v = (1+juros)**-1
  t <- (1:(length(pxx)))
  return(sum(v^(t)*pxx))
}

# ANUIDADE POSTECIPADA VITALICIA E DIFERIDA -------------------------------
a_post_vit_dif = function(tabua = 'AT_49_F', idade, juros, dif){
  qx = qx[, tabua]
  qx[is.na(qx)] = 1
  v = (1+juros)**-1
  px = 1-qx
  dotal = v**dif * prod(px[(idade+1):(idade+dif)])
  pxx = c(cumprod(px[(idade+1+dif):length(px)]))
  t <- (1:(length(pxx)))
  return(dotal * sum(v^(t)*pxx))
}

# ANUIDADE POSTECIPADA TEMPORARIA -----------------------------------------
a_post_temp = function(tabua = 'AT_49_F', idade, juros, n){
  qx = qx[, tabua]
  qx[is.na(qx)] = 1
  v = (1+juros)**-1
  px = 1-qx
  pxx = cumprod(px[(idade+1):(idade+n)])
  t <- (1:n)
  return(sum(v^(t)*pxx))
}

# ANUIDADE POSTECIPADA TEMPORARIA E DIFERIDA ------------------------------
a_post_temp_dif = function(tabua = 'AT_49_F', idade, juros, n, dif){
  qx = qx[, tabua]
  qx[is.na(qx)] = 1
  v = (1+juros)**-1
  px = 1-qx
  dotal = v**dif * prod(px[(idade+1):(idade+dif)])
  pxx = cumprod(px[(idade+1+dif):(idade+dif+n)])
  t <- (1:n)
  return(dotal * sum(v^(t)*pxx))
}


