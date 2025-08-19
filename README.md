PLEASE UPDATE ME !!!

Download to 3 CSV files, please locate in the "CSV's" folder/directory 
https://drive.google.com/drive/folders/17TLKcEXsFTH8LSM5-rsFEmBEXiBjTsNQ?usp=drive_link

The final models are already selected.
If require just the webapp, please follow this order 

- RUN WITH MODELS SELECTED - 

To create the databases please run 
1) create_dbs.py

To create the encrytion key please run 
1) gen_key.py

To start the website please run
1) app.py 
2) open http://127.0.0.1:5000 on your browser 

To run all the code from fresh please run in this order.

- TO RUN ALL FOLLOW THIS ORDER -

After doing so, please run in this order to clean data. 
1) clean_train_data.py
2) clean_pollution.py

To create the encrytion key please run 
1) gen_key.py

To create the databases please run 
1) create_dbs.py

To train the all models please run (best option)
1) models_all.py
2) please make sure 7 models have been moved to "/static/final_models" folder
3) IF NOT, PLEASE RUN best_models.py 

To train the models individually please run (optional)
1) LR_model.py/FR_model.py/XGB_model.py 
2) best_models.py 
3) If you would want only one model just run one of three above

To create graphs of the models performance please run
1) graphs.py
2) to review graphs please view "/results/graphs"

To start the website please run
1) app.py 
2) open http://127.0.0.1:5000 on your browser 


------- TESTS -------
Please run all above first ! 
Then please run the tests, however for time sake please do not run test_models_all.
This test will take arround 20 minuates to run as it is retraining the models, this is making sure the output is what i expect.


