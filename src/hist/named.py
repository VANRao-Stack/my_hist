from .core import BaseHist
import matplotlib.pyplot as plt
import seaborn
import numpy as np


class NamedHist(BaseHist):
    def fill(self, *args, **kwargs):
        """

        Insert data into the histogram.



        Parameters

        ----------

        *args : Union[Array[float], Array[int], Array[str], float, int, str]

            Provide one value or array per dimension.

        **kwargs : Used similar to args but however gives the flexibilty to

            fill values into axes using their names instead of their index.

        weight : List[Union[Array[float], Array[int], Array[str], float, int, str]]]

            Provide weights (only if the histogram storage supports it)

        NOTE: the weight keyword is not explicitly mentioned in the call to the

            function but however is instead stored inside kwargs from where it is passed on.

            

        """
        
        #Checking the format of the input and passing it to the super().fill() function if it is in any of the old formats
        if len(args) != 0:
            if 'weight' in kwargs:
                BaseHist.fill(self, *args, kwargs['weight'])
            else:
                BaseHist.fill(self, *args)

        #If the user used the keyword augmented arguments then the input is aranged according to the order of the
        #axes and then passed to the super().fill() function        
        else:
            temp_list = list()
            for value in self.axes:
                temp_list.append(kwargs[value.name])
            if 'weight' not in kwargs:
                kwargs['weight'] = None
            BaseHist.fill(self, *temp_list, weight=kwargs['weight'])


    def pull_plot(self, pdf, *, ax=None, pull_ax=None, style='seaborn-deep', figsize=(6, 8), save_fig=None):

        """

        Used to plot the count and the pull plot of a particular axis given. For more details regarding the
        extension of the function to more genral cases please refer to the readme file in the repository.


        Paramters

        ---------

        pdf : the equation of the PDF to be plotted, in the example given a Gaussian distribution was

            used

        ax : The axis used to make the figure of the pdf and the scatter plot of the points

        pull_ax : The axis used to make the figure of the pull plot

        style : The style of the plot, by default it is the Seaborn-Deep but however can be reverted to more

            informative plots by passing the required argument

        figsize : a tuple that is used to determine the size of the figure

        save_fig : the title for the figure if it is to be saved. Note that it will be saved as a png

            hence adding an extension in not required

        Process

        -------

        The function takes the above arguments and then plots the two figures, that is, the pdf along with
        the points as well as a pull plot of the same. Note that this fucntion is only capable of producing
        plots for one dimensional plots and not for the multi dimensional case. For more information on how
        this function could be extended can be found in the readme.

        Output

        ------

        ax : The axis that was either passed into the function or the one produced for the pdf

        pull_ax : The axis that was either passed into the function or the one that was produced

            for the pull plot.

            
        """
        #Calculating the values of the pdf
        values = pdf(*self.axes.centers)*self.sum()*self.axes[0].widths
        yerr = np.sqrt(self.view())

        #calculating the pulls
        pulls = (self.view() - values) / yerr

        #checking and creating the two axes if required
        if ax is None and pull_ax is None:
            fig, (ax, pull_ax) = plt.subplots(2, 1, gridspec_kw={'height_ratios': [3, 1]}, figsize=figsize)
        elif ax is None or pull_ax is None:
            print('Please enter both the axes or none of them!')
            return None, None

        #plotting the pdf
        ax.errorbar(self.axes[0].centers, values);

        #plotting the scatter plot on the pdf
        ax.scatter(self.axes[0].centers, self.view(), s=self.view(), marker='|');
        ax.scatter(self.axes[0].centers, self.view(), s=10, marker='D', color='orange')

        #Setting the labels for the pdf plot
        ax.set_xlabel('x[units]')
        ax.set_ylabel(self.axes[0].name)

        #plotting the pulls
        pull_ax.bar(self.axes[0].centers, pulls, width=self.axes[0].widths);
        seaborn.despine(ax=pull_ax, offset=10, trim=True)

        #setting the labels for the pull plot
        pull_ax.set_xlabel('x[units]')
        pull_ax.set_ylabel('Pulls')

        #adding informative coloring on to the pull plot
        for i in range(1, int(max(pulls))):
            pull_ax.axhspan(-i, i, color='b', alpha=0.05)

        #styling the plots and then finally displaying
        plt.style.use(style)
        fig.tight_layout()
        plt.show()

        #saving the figure
        if save_fig is not None:
            fig.save_fig(save_fig + '.png')
        
        #returning the newly built or passed plots
        return ax, pull_ax


    def __getitem__(self, index):

        """

        Used to access the different axes objects within the Histogram



        Parameters

        ----------

        index : this could be a integer a list or even a dictionary. It is used

            access and return multiple or single even no axes.

        Output

        ------

        Return the axes that was called upon. 
        
        """
        
        #Here, first its checked whther the input is any of the old formats and then passed to the super().__getitem__() if its so
        if type(index) != dict:
            return BaseHist.__getitem__(self, index)
        if set(map(type, index)) == {int}:
            return BaseHist.__getitem__(self, index)

        #If however its not then looping is used to convert the new format to an older one in order to pass it throught to the super().__getitem() function
        temp_dict = dict()
        for ind, val in enumerate(self.axes):
            if val.name in index.keys():
                temp_dict[ind] = index[val.name]
        return BaseHist.__getitem__(self, temp_dict)

        
        
    def __setitem__(self, index, value):
        
        """
        Used to set the value of different values in the histogram
        
        Parameters
        ----------
        
        index: formatted similar to that of the getitem, it specifies which of the given values is to be set
        
        value: the value to be set for the particular object
        
        """
        
        #check if instance of dict
        if isinstance(index, dict):
            
            #if it is then modification to current format is maybe required
            k = list(index.keys())
            
            #check if the keys are string
            if isinstance(k[0], str):
                
                #if they are then modicfication is definetly required
                for key in k:
                    
                    #perform those modifications to conver it to a format that's understood by the super.__setitem__() function
                    for ind, axis in enumerate(self.axes):
                        if key == axis.name:
                            index[ind] = index.pop(key)
                            break

        return super().__setitem__(index, value)
