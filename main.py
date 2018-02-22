from Environment.environment import Environment


if __name__ == "__main__":
   env = Environment(maxgenerations=400,
                     size= 200 ,
                     optimum= 80)
   env.run()
