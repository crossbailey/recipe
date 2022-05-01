# recipe

# Tasty
            result_ingr = recipe_driver.find_element(by=By.XPATH, value="//*[@id='content']/div[1]/div/div[4]/div[1]/div[1]").text
            result_instruct = recipe_driver.find_element(by=By.XPATH, value="//*[@id='content']/div[1]/div/div[4]/div[1]/div[2]/ol").text
            recipe_driver.close()

            # Whisk
            result_ingr = recipe_driver.find_element(by=By.XPATH, value="//*[@id='app']/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[3]/div/div").text
            result_instruct = recipe_driver.find_element(by=By.XPATH, value="//*[@id='app'']/div[2]/div[1]/div/div[2]/div[2]/div[3]/div[1]/div").text
            recipe_driver.close()

            # Simply Recipes
            result_ingr = recipe_driver.find_element(by=By.XPATH, value="/html/body/main/article/div[1]/div/div[2]/div[2]/section[1]/div/div[1]/ul").text
            result_instruct = recipe_driver.find_element(by=By.XPATH, value="//*[@id='mntl-sc-block_3-0']").text
            recipe_driver.close()
