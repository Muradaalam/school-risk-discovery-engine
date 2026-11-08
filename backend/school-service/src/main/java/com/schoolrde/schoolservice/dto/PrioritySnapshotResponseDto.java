package com.schoolrde.schoolservice.dto;

import java.sql.Date;

public class PrioritySnapshotResponseDto{

	private Integer id;
    private Date snapshotDate;
    private Integer priorityScore;
    private Integer activeIssues;
    private Integer underResolutionIssues;
    private Integer resolvedIssues;
	
    public Integer getId(){
		return id;
	}

	public void setId(Integer id){
		this.id = id;
	}

	public Date getSnapshotDate(){
		return snapshotDate;
	}

	public void setSnapshotDate(Date snapshotDate){
		this.snapshotDate = snapshotDate;
	}

	public Integer getPriorityScore(){
		return priorityScore;
	}

	public void setPriorityScore(Integer priorityScore){
		this.priorityScore = priorityScore;
	}

	public Integer getActiveIssues(){
		return activeIssues;
	}

	public void setActiveIssues(Integer activeIssues){
		this.activeIssues = activeIssues;
	}

	public Integer getUnderResolutionIssues(){
		return underResolutionIssues;
	}

	public void setUnderResolutionIssues(Integer underResolutionIssues){
		this.underResolutionIssues = underResolutionIssues;
	}

	public Integer getResolvedIssues(){
		return resolvedIssues;
	}

	public void setResolvedIssues(Integer resolvedIssues){
		this.resolvedIssues = resolvedIssues;
	}

}