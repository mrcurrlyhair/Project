PLEASE UPDATE ME !!!

Download to 3 CSV files, please locate in the "CSV's" folder
https://drive.google.com/drive/folders/17TLKcEXsFTH8LSM5-rsFEmBEXiBjTsNQ?usp=drive_link

- FOLLOW THIS ORDER -

After doing so, please run in this order to clean data. 
1) clean_train_data.py
2) clean_pollution.py

To create the encrytion key please run 
1) gen_key.py


To create the databases please run 
1) create_dbs.py

To train the all models please run 
1) models_all.py
2) please make sure 7 models have been moved to "/static/final_models" folder
3) IF NOT, PLEASE RUN best_models.py 

To train the models individually please run (NOTE: running these three at the same time is faster than models_all.py!)
1) LR_model.py/FR_model.py/XGB_model.py 
2) best_models.py 
3) If you would want only one model just run one of three above

To create feature graphs please run
1) graphs.py

To start the website please run
1) app.py 
2) open http://127.0.0.1:5000 on your browser 


------- TESTS -------
Please run all above first ! 
Then please run the tests, however for time sake please do not run test_models_all.
This test will take arround 20 minuates to run as it is retraining the models, this is making sure the output is what i expect.

