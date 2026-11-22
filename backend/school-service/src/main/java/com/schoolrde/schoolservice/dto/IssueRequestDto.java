package com.schoolrde.schoolservice.dto;

import java.sql.Date;

public class IssueRequestDto{

	private Integer id;
	private Integer schoolId;
	private Integer issueTypeId;
	private Integer statusId;
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

	public Integer getIssueTypeId(){
	    return issueTypeId;
	}

	public void setIssueTypeId(Integer issueTypeId){
	    this.issueTypeId = issueTypeId;
	}

	public Integer getStatusId(){
	    return statusId;
	}

	public void setStatusId(Integer statusId){
	    this.statusId = statusId;
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