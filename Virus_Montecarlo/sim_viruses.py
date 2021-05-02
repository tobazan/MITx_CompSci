import random
import pylab

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus to indicate that a virus particle doesn't reproduce.
    """

class SimpleVirus(object):
    """
    Rep of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb        

    def getMaxBirthProb(self):
        return self.maxBirthProb

    def getClearProb(self):
        return self.clearProb

    def doesClear(self):
        """ Stochastically determines whether this virus particle is 
        cleared from the patient's body at a time step.

        Returns: True with probability self.getClearProb and otherwise
        returns False.
        """
        x = random.random()
        
        clear = x < self.clearProb

        return clear

    
    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces 
        at a time step. Called by the update() method in the Patient and
        TreatedPatient classes. The virus particle reproduces with prob
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and 
        returns the instance of the offspring SimpleVirus (which has the 
        same maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        Returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        repProb = self.maxBirthProb * (1 - popDensity)
        x = random.random()

        if x < repProb:
            return SimpleVirus(self.maxBirthProb, self.clearProb)
        else:
            raise NoChildException


class Patient(object):
    """
    Representation of a simplified patient. The patient does not take 
    any drugs and his/her virus populations have no drug resistance.
    """    

    def __init__(self, viruses, maxPop):
        """
        viruses: list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the max virus population for this patient (an integer)
        """
        self.viruses = viruses
        self.maxPop = maxPop

    def getViruses(self):
        return self.viruses

    def getMaxPop(self):
        return self.maxPop

    def getTotalPop(self):
        """
        Gets the size of the current total virus population. 
        returns: The total virus population (an integer)
        """
        return len(self.viruses)        

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step.
        
        - Determine whether each virus particle survives and updates the list.   
        
        - The current pop density is calculated. This value is used until the
        next call to update() 
        
        - Based on pop density, determine whether each virus particle should
        reproduce and add offspring virus particles to viruses in this patient.                    

        Returns: The total virus population at the end of the update
        """
        updated_viruses = []
        for i in self.viruses:
            if not i.doesClear():
                updated_viruses.append(i)

        current_pop = self.getTotalPop() / self.getMaxPop()

        offsprings = []
        for i in updated_viruses:
            try:
                off_virus = i.reproduce(current_pop)
                offsprings.append(off_virus)
            except NoChildException:
                pass

        self.viruses = updated_viruses + offsprings
        return

def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials):
    result = [ [] for t in range(300) ]
    
    for trial in range(numTrials):
        viruses = [SimpleVirus(maxBirthProb, clearProb) for v in range(numViruses)]
        person = Patient(viruses, maxPop)
        
        for step in range(300):
            person.update()
            result[step].append(person.getTotalPop())
            
    y = [ sum(r)/numTrials for r in result]
        
    # pylab.plot(y, label = "SimpleVirus")
    # pylab.title("SimpleVirus simulation")
    # pylab.xlabel("Time Steps")
    # pylab.ylabel("Average Virus Population")
    # pylab.legend(loc = "best")
    
    # return  pylab.show()
    return y

class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """   

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)       

        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'srinol':False}, means that this virus
        particle is resistant to neither guttagonol nor srinol.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.
        """
        SimpleVirus.__init__(self, maxBirthProb, clearProb)

        self.resistances = resistances
        self.mutProb = mutProb      

    def getResistances(self):
        """
        Returns the resistances for this virus.
        """
        return self.resistances

    def getMutProb(self):
        """
        Returns the mutation probability for this virus.
        """
        return self.mutProb

    def isResistantTo(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in TreatedPatient to determine how many virus
        particles have resistance to a drug.       

        drug: The drug (a string)

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        res = self.resistances
        return res.get(drug)

    def reproduce(self, popDensity, activeDrugs):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the TreatedPatient class.

        A virus particle will only reproduce if it is resistant to ALL the drugs
        in the activeDrugs list. For example, if there are 2 drugs in the
        activeDrugs list, and the virus particle is resistant to 1 or no drugs,
        then it will NOT reproduce.

        Hence, if the virus is resistant to all drugs
        in activeDrugs, then the virus reproduces with probability:      

        self.maxBirthProb * (1 - popDensity).                       

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). The offspring virus
        will have the same maxBirthProb, clearProb, and mutProb as the parent.

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.       

        For example, if a virus particle is resistant to guttagonol but not
        srinol, and self.mutProb is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        srinol and a 90% chance that the offspring will not be resistant to
        srinol.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population       

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """
        res = []
        for drug in activeDrugs:
            res.append(self.resistances.get(drug))

        if False not in res and None not in res:
            repProb = self.maxBirthProb * (1 - popDensity)
            x = random.random()

            if x < repProb:

                m_res = {}

                for k, v in self.resistances.items():
                    if v == True:
                        if x < 1 - self.mutProb:
                            m_res[k] = True
                        else: 
                            m_res[k] = False
                    else:
                        if x < 1 - self.mutProb:
                            m_res[k] = False
                        else:
                            m_res[k] = True
                        
                return ResistantVirus(self.maxBirthProb, self.clearProb, m_res, self.mutProb)

            else:
                raise NoChildException

class TreatedPatient(Patient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).              

        viruses: The list representing the virus population (a list of
        virus instances)

        maxPop: The  maximum virus population for this patient (an integer)
        """

        Patient.__init__(self, viruses, maxPop)
        self.prescripted = []

    def addPrescription(self, newDrug):
        """
        After a prescription is added, the drug acts on the virus population 
        for all subsequent time steps. If the newDrug is already prescribed 
        to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        post: Updates the list of drugs being administered to the patient
        """
        if newDrug not in self.prescripted:
            self.prescripted.append(newDrug)
        
        return

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered
        """
        return self.prescripted

    def getResistPop(self, drugResist):
        """
        Get the population of virus resistant to the drugs listed in drugResist.       

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'srinol'])

        returns: The population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistant_pop = 0

        for v in self.viruses:
            r = [ v.isResistantTo(d) for d in drugResist ]
            if False not in r and None not in r:
                resistant_pop += 1
        
        return resistant_pop

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
        virus particles accordingly

        - The current population density is calculated. This population density
        value is used until the next call to update().

        - Based on this value of population density, determine whether each 
        virus particle should reproduce and add offspring virus particles to 
        the list of viruses in this patient.
        The list of drugs being administered should be accounted for in the
        determination of whether each virus particle reproduces.

        returns: The total virus population at the end of the update (an
        integer)
        """

        updated_viruses = []
        for i in self.viruses:
            if not i.doesClear():
                updated_viruses.append(i)

        current_pop = self.getTotalPop() / self.getMaxPop()

        offsprings = []
        for i in updated_viruses:
            try:
                off_virus = i.reproduce(current_pop, self.prescripted)
                if off_virus != None:
                    offsprings.append(off_virus)
            except NoChildException:
                pass
        
        self.viruses = updated_viruses + offsprings
        return

def simulationWithDrug(numViruses, maxPop, maxBirthProb, clearProb, resistances, mutProb, numTrials):
    """
    Runs simulations and plots graphs for problem 5.

    For each of numTrials trials, instantiates a patient, runs a simulation for
    150 timesteps, adds guttagonol, and runs the simulation for an additional
    150 timesteps.  At the end plots the average virus population size
    (for both the total virus population and the guttagonol-resistant virus
    population) as a function of time.

    numViruses: number of ResistantVirus to create for patient (an integer)
    maxPop: maximum virus population for patient (an integer)
    maxBirthProb: Maximum reproduction probability (a float between 0-1)        
    clearProb: maximum clearance probability (a float between 0-1)
    resistances: a dictionary of drugs that each ResistantVirus is resistant to
                (e.g., {'guttagonol': False})
    mutProb: mutation probability for each ResistantVirus particle
            (a float between 0-1). 
    numTrials: number of simulation runs to execute (an integer)
    
    """
    total = [ [] for t in range(300) ]
    resistant = [ [] for t in range(300) ]

    for trial in range(numTrials):
        viruses = [ResistantVirus(maxBirthProb, clearProb, resistances, mutProb) for v in range(numViruses)]
        person = TreatedPatient(viruses, maxPop)
        
        for step in range(150):
            person.update()
            total[step].append(person.getTotalPop())
            resistant[step].append(person.getResistPop(['guttagonol']))
        
        person.addPrescription('guttagonol')

        for step in range(150,300):
            person.update()
            total[step].append(person.getTotalPop())
            resistant[step].append(person.getResistPop(['guttagonol']))

    y_total = [ sum(r)/numTrials for r in total]
    y_resistant = [ sum(r)/numTrials for r in resistant]

    # pylab.plot(y_total, label = "Total Pop")
    # pylab.plot(y_resistant, label = "Resistant Pop")
    # pylab.title("ResistanVirus simulation")
    # pylab.xlabel("Time Steps")
    # pylab.ylabel("Average Virus Population")
    # pylab.legend(loc = "best")
    
    # return  pylab.show()
    return (y_total, y_resistant)
