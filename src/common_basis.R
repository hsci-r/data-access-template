library(here)
library(tidyverse)
library(hscidbutil)
library(keyring)
library(DBI)
library(RMariaDB)
library(googlesheets4)
library(yaml)

get_connection <- function() {
  while (!exists("con")) {
    db_params <- read_yaml(here("db_params.yaml"))
    tryCatch(con <- dbConnect(
      drv = MariaDB(),
      host = db_params$db_host,
      dbname = db_params$db_name,
      user = db_params$db_user,
      password = if (file.exists(here("db_secret.yaml"))) read_yaml(here("db_secret.yaml"))$db_pass else key_get(db_params$db_name,"DB_PASS"),
      bigint = "integer",
      load_data_local_infile = TRUE,
      autocommit = TRUE,
      reconnect = TRUE
    ), error = function(e) {
      print(e)
      key_set(db_params$db_name,"DB_PASS", prompt="Database password: ")
    })
  }
  con
}

con <- get_connection()
rm(get_connection)

try(test_a <- tbl(con, "test_a"))
try(test_c <- tbl(con, "test_c"))

