package com.schoolrde.schoolservice.dto;

import java.sql.Date;

public class IssueRequestDto{

	private Integer id;
	private Integer schoolId;
	private String issueType;
	private String issueStatus;
	private Date firstDetected;
	private Date lastUpdated;
	private Date resolvedAt;

	// Getters and setters are generated using STS: Source > Generate Getters and Setters
	public Integer getId(){
	    return id;
	}

	public void setId(Integer id){
	    this.id = id;
	}

	public Integer getSchoolId(){
	    return schoolId;
	}

	public void setSchoolId(Integer schoolId){
	    this.schoolId = schoolId;
	}

	public String getIssueType(){
	    return issueType;
	}

	public void setIssueTypeId(String issueType){
	    this.issueType = issueType;
	}

	public String getIssueStatus(){
	    return issueStatus;
	}

	public void setIssueStatus(String issueStatus){
	    this.issueStatus = issueStatus;
	}

	public Date getFirstDetected(){
	    return firstDetected;
	}

	public void setFirstDetected(Date firstDetected){
	    this.firstDetected = firstDetected;
	}

	public Date getLastUpdated(){
	    return lastUpdated;
	}

	public void setLastUpdated(Date lastUpdated){
	    this.lastUpdated = lastUpdated;
	}

	public Date getResolvedAt(){
	    return resolvedAt;
	}

	public void setResolvedAt(Date resolvedAt){
	    this.resolvedAt = resolvedAt;
	}
}