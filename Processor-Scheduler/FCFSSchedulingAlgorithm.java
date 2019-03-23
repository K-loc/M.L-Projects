/** FCFSSchedulingAlgorithm.java
 * 
 * A first-come first-served scheduling algorithm.
 *
 * @author: Charles Zhu
 * Spring 2016
 *
 */
package com.jimweller.cpuscheduler;

import java.util.*;

public class FCFSSchedulingAlgorithm extends BaseSchedulingAlgorithm {

    private Vector<Process> jobs;
    
    FCFSSchedulingAlgorithm(){
        activeJob = null;
        jobs = new Vector<Process>();
    }

    /** Add the new job to the correct queue.*/
    public void addJob(Process p){ //utilizes binary search to find slots to add based on arrival time
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
        if (activeJob != null && activeJob.isFinished() != true) //non-preemptive
        	return activeJob; //makes sure active process is done before switch
        Collections.sort(jobs, new SortbyArrival()); //sorting jobs so shortest jobs first
        activeJob = jobs.get(0); //compare proposed with other PIDS with same arrival
		return activeJob;    
    }

    public String getName(){
        return "First-Come First-Served";
    }
}

class SortbyArrival implements Comparator<Process>
{
    public int compare(Process a, Process b)
    {
        if (a.getArrivalTime() < b.getArrivalTime()) //if a less than, put before b
            return -1;
        else if (a.getArrivalTime() == b.getArrivalTime())
        	if (a.getPID() < b.getPID()) //if equal, check for PID
            	return -1;
            else
            	return 1;
        else //if a is greater than, put after b
            return 1;
    }
}