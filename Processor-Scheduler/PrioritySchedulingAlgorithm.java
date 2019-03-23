/** PrioritySchedulingAlgorithm.java
 * 
 * A single-queue priority scheduling algorithm.
 *
 * @author: Charles Zhu
 * Spring 2016
 *
 */
package com.jimweller.cpuscheduler;

import java.util.*;

import com.jimweller.cpuscheduler.Process;

public class PrioritySchedulingAlgorithm extends BaseSchedulingAlgorithm implements OptionallyPreemptiveSchedulingAlgorithm {
    
    private Vector<Process> jobs;
    private boolean preemptive;

    PrioritySchedulingAlgorithm(){
        activeJob = null;
        jobs = new Vector<Process>();
        preemptive = false;
    }

    /** Add the new job to the correct queue.*/
    public void addJob(Process p){
        jobs.add(p);
    }
    
    /** Returns true if the job was present and was removed. */
    public boolean removeJob(Process p){
        return jobs.remove(p);
    }

    /** Transfer all the jobs in the queue of a SchedulingAlgorithm to another, such as
    when switching to another algorithm in the GUI */
    public void transferJobsTo(SchedulingAlgorithm otherAlg) {
        throw new UnsupportedOperationException();
    }


    /** Returns the next process that should be run by the CPU, null if none available.*/
    public Process getNextJob(long currentTime){
        if (preemptive == false) { //non preemptive
            if (activeJob != null && activeJob.isFinished() != true) //non-preemptive
                return activeJob; //makes sure active process is done before switch
             //if no active job or active job is complete, switch
            Collections.sort(jobs, new SortbyPriority());
            activeJob = jobs.get(0);
            return activeJob;
        }
        
        else { //preemptive
            Collections.sort(jobs, new SortbyPriority());
            activeJob = jobs.get(0);
            return activeJob;
        }

        /*------------------------------------------------------------*/
    }

    public String getName(){
        return "Single-Queue Priority";
    }

    /**
     * @return Value of preemptive.
     */
    public boolean isPreemptive(){
        return preemptive;
    }
    
    /**
     * @param v Value to assign to preemptive.
     */
    public void setPreemptive(boolean v){
        this.preemptive = v;
    }    
}

class SortbyPriority implements Comparator<Process>
{
    public int compare(Process a, Process b)
    {
        if (a.getPriorityWeight() < b.getPriorityWeight())
            return -1;
        else if (a.getPriorityWeight() == b.getPriorityWeight())
            if (a.getPID() < b.getPID())
                return -1;
            else
                return 1;
        else
            return 1;
    }
}