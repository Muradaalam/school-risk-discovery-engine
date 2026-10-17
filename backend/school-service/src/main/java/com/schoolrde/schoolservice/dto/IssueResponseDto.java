package com.schoolrde.schoolservice.dto;

import java.sql.Date;

public class IssueResponseDto{

    private Integer id;
    private Integer issueTypeId;
    private String issueType;
    private String issueTypeDescription;
    private Integer statusId;
    private String status;
    private String statusDescription;
    private Date firstDetected;
    private Date lastUpdated;
    private Date resolvedAt;

    public Integer getId(){
        return id;
    }

    public void setId(Integer id){
        this.id = id;
    }

    public Integer getIssueTypeId(){
        return issueTypeId;
    }

    public void setIssueTypeId(Integer issueTypeId){
        this.issueTypeId = issueTypeId;
    }

    public String getIssueType(){
        return issueType;
    }

    public void setIssueType(String issueType){
        this.issueType = issueType;
    }

    public String getIssueTypeDescription(){
        return issueTypeDescription;
    }

    public void setIssueTypeDescription(String issueTypeDescription){
        this.issueTypeDescription = issueTypeDescription;
    }

    public Integer getStatusId(){
        return statusId;
    }

    public void setStatusId(Integer statusId){
        this.statusId = statusId;
    }

    public String getStatus(){
        return status;
    }

    public void setStatus(String status){
        this.status = status;
    }

    public String getStatusDescription(){
        return statusDescription;
    }

    public void setStatusDescription(String statusDescription){
        this.statusDescription = statusDescription;
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