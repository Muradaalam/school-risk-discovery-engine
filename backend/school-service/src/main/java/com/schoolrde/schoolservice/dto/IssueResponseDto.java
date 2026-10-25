package com.schoolrde.schoolservice.dto;

import java.sql.Date;
import java.util.List;

public class IssueResponseDto{

    private Integer id;
    private String issueType;
    private String issueTypeDescription;
    private String status;
    private String statusDescription;
    private Date firstDetected;
    private Date lastUpdated;
    private Date resolvedAt;
    private List<ProjectResponseDto> projects;


    public Integer getId(){
        return id;
    }

    public void setId(Integer id){
        this.id = id;
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
    
    public List<ProjectResponseDto> getProjects() {
        return projects;
    }

    public void setProjects(List<ProjectResponseDto> projects) {
        this.projects = projects;
    }

}