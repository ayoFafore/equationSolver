import random
import streamlit as st
import pandas as pd


class Chromosome:
    def __init__(self, gene, fitness):
        self.gene = gene
        self.fitness = fitness


class Population:
    def __init__(self, population_size, target):
        self.chromosomes = []
        self.population_size = population_size
        self.target = target

    def generate_population_with_gene_size(self, gene_size):
        for x in range(self.population_size):
            gene = random.sample(range(self.target), gene_size)
            fitness = get_fitness(gene, self.target)
            chromosome = Chromosome(gene, fitness)
            self.chromosomes.append(chromosome)

    def breed_population(self, survival_rate):
        self.chromosomes.sort(key=lambda c: c.fitness)
        self.chromosomes = self.chromosomes[:survival_rate]

        while len(self.chromosomes) < self.population_size:
            parent_1 = random.choice(self.chromosomes)
            parent_2 = random.choice(self.chromosomes)
            child = self.breed_parents(parent_1, parent_2)
            self.chromosomes.append(child)

    def breed_parents(self, parent_1, parent_2):
        child_gene = []
        for i in range(len(parent_1.gene)):
            flip = random.uniform(0, 1)
            if flip > .5:
                child_gene.append(parent_1.gene[i])
            else:
                child_gene.append(parent_2.gene[i])
        return Chromosome(child_gene, get_fitness(child_gene, self.target))


def get_fitness(gene, target):
    total = 0
    var = 1
    for g in gene:
        total += var * g
        var += 1
    diff = abs(target - total) / 1
    return diff


def get_result(gene):
    res = ''
    var = 1
    sum = 0
    for g in gene:
        res += '{x}*{num}+'.format(x=var, num=g)
        sum += var * g
        var += 1

    return res.rstrip(res[-1]), sum


st.header('Solving equation with genetic algorithm')
pop_size = int(st.number_input('Insert Population Size'))
target_number = int(st.number_input('Insert The Target Number'))
p = Population(pop_size, target_number)
max_iterations = int(st.number_input('Insert The Maximum Allowed Iterations'))
gene_size = int(st.number_input('Insert gene size'))
top_chromosome = None
if st.button('Run'):
    p.generate_population_with_gene_size(gene_size)
    fitness_per_population = []
    generation = []
    total_number_of_iterations = 1
    for i in range(max_iterations + 1):
        total_number_of_iterations = i
        p.breed_population(10)
        fitness_per_population.append([c.fitness for c in p.chromosomes])
        generation.append(i)
        top_chromosome = p.chromosomes[0]
        if top_chromosome.fitness == 0:
            break

    st.subheader('Chart of Fitness Over Generations')
    df = pd.DataFrame(
        fitness_per_population, generation)
    st.line_chart(df)

    expression, total = get_result(top_chromosome.gene)
    st.write('Result After {iter} Iterations'.format(iter=total_number_of_iterations))
    st.latex(r'''
        {expr} = {res}
        '''.format(expr=expression, res=total))
