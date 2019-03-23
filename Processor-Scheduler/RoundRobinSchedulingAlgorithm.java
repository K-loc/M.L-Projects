/** RoundRobinSchedulingAlgorithm.java
 * 
 * A scheduling algorithm that randomly picks the next job to go.
 *
 * @author: Kyle Benson
 * Winter 2013
 *
 */
package com.jimweller.cpuscheduler;

import java.util.*;

public class RoundRobinSchedulingAlgorithm extends BaseSchedulingAlgorithm {

    /** the time slice each process gets */
    private int quantum;
    private Vector<Process> jobs;
    private int count;
    private int timer;

    RoundRobinSchedulingAlgorithm() {
        activeJob = null;
        jobs = new Vector<Process>();
        quantum = 9;
        count = 0;
        timer = 0;
    }

    /** Add the new job to the correct queue. */
    public void addJob(Process p) {
    	jobs.add(p);
    }

    /** Returns true if the job was present and was removed. */
    public boolean removeJob(Process p) {
        // Remove the next lines to start your implementation
        return jobs.remove(p);
    }

    /** Transfer all the jobs in the queue of a SchedulingAlgorithm to another, such as
    when switching to another algorithm in the GUI */
    public void transferJobsTo(SchedulingAlgorithm otherAlg) {
        throw new UnsupportedOperationException();
    }

    /**
     * Get the value of quantum.
     * 
     * @return Value of quantum.
     */
    public int getQuantum() {
        return quantum;
    }

    /**
     * Set the value of quantum.
     * 
     * @param v
     *            Value to assign to quantum.
     */
    public void setQuantum(int v) {
        this.quantum = v-1;
    }

    /**
     * Returns the next process that should be run by the CPU, null if none
     * available.
     */
    public Process getNextJob(long currentTime) {
        if (timer < quantum) { //whenever you arent in quantum
            if (activeJob != null && activeJob.isFinished() == false) { 
                timer += 1;
                return activeJob; //if there is a job, continue
            }
            else { //if active is null or is finished
                timer = 0;
                nextAvail();
                return activeJob;
            }
        }
        else { //if in quantum
            timer = 0;
            nextAvail();
            return activeJob;
        }
    }

    public String getName() {
        return "Round Robin";
    }

    private void nextAvail() {
        Collections.sort(jobs, new SortByPID());
        count = count % jobs.size(); //in the case that last index is removed
        if (activeJob == null || activeJob.getPID() != jobs.get(count).getPID())
            activeJob = jobs.get(count); //if there is a removal, do not change index
        else {
            count = (count+1) %jobs.size(); //in the case that +1 goes over size
            activeJob = jobs.get(count);
        }
    }

    private void print_jobs() {
        System.out.println("Printing jobs");
        for (int i = 0; i < jobs.size(); ++i) {
            jobs.get(i).println();

        }
    }

}

class SortByPID implements Comparator<Process>
{
    public int compare(Process a, Process b)
    {
        if (a.getPID() < b.getPID())
            return -1;
        else if (a.getPID() > b.getPID())
            return 1;
        return 0;
    }
}