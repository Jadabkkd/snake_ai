# Snake Ai with Genetic Algorithm
From **Charles Darwin's theory** + **Pygame** and now it become to Snake Ai.
<br>
<br>
![](https://github.com/Jadabkkd/snake_ai/blob/main/snake_ai.gif)
# Running
run app.py

Or if you need customize go to play around with setting.py. You can setup both of neural net property and genetic algo property also,and make sure that you're setting **use_pretrained = Flase**,

For faster training process can go to check with pseudo_training similar setting but no rendering.
# Pipeline

```mermaid
stateDiagram
	GerneratePop
    GerneratePop --> Selection
    Selection--> Crossover
    Crossover --> Mutation
    Mutation --> GerneratePop 
```

# My best setting so far...
 - in settings.py<br>
	self.use_pretrained = True<br>
	self.classification = ["L","R","U","D"]<br>
	self.Populations = 1500<br>
	self.Parents = 500<br>
	self.NetworkLayers = [28,22,4]<br>
	self.initPopType = 'Xavier'<br>
	self.ActivationFunction_hdl = 'ReLu'<br>
	self.ActivationFunction_output = 'Softmax'<br>
	self.SelectionType = ['Roulette']<br>
	self.CrossoverType = ['SBX','SPX']<br>
	self.MutationType = ['Gaussian','Uniform']<br>
	self.mutation_prop = 0.05<br>
