package com.jimweller.cpuscheduler;

import java.util.*;

import com.jimweller.cpuscheduler.Process;

public class SJFSchedulingAlgorithm extends BaseSchedulingAlgorithm implements OptionallyPreemptiveSchedulingAlgorithm {
    
    private Vector<Process> jobs;
    private boolean preemptive;

    SJFSchedulingAlgorithm(){
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
        if (preemptive == false) { //non-preemptive
            if (activeJob != null && activeJob.isFinished() != true) //non-preemptive
                return activeJob; //makes sure active process is done before switch
             //if no active job or active is complete, change job
            Collections.sort(jobs, new SortbyInitBurst());
            activeJob = jobs.get(0);
            return activeJob;
        }
        
        else { //preemptive
            Collections.sort(jobs, new SortbyBurst()); //switch the process to the first index always
            activeJob = jobs.get(0);
            return activeJob;
        }
    }

    public String getName(){
        return "Shortest Job First";
    }

    /**
     * @return Value of preemptive.
     */
    public boolean isPreemptive(){
        return preemptive;
    }
    
    /**
     * @param v  Value to assign to preemptive.
     */
    public void setPreemptive(boolean v){
        this.preemptive = v; 
    }
}

class SortbyBurst implements Comparator<Process>
{
    public int compare(Process a, Process b)
    {
        if (a.getBurstTime() < b.getBurstTime() )
            return -1;
        else if (a.getBurstTime() == b.getBurstTime())
            if (a.getPID() < b.getPID())
                return -1;
            else
                return 1;
        else
            return 1;
    }
}

class SortbyInitBurst implements Comparator<Process>
{
    public int compare(Process a, Process b)
    {
        if (a.getInitBurstTime() < b.getInitBurstTime() )
            return -1;
        else if (a.getInitBurstTime() == b.getInitBurstTime() )
            if (a.getPID() < b.getPID())
                return -1;
            else
                return 1;
        else
            return 1;
    }
}
