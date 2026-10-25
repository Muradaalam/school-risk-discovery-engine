package com.schoolrde.schoolservice.dto;

import java.math.BigDecimal;
import java.sql.Date;
import java.time.LocalDate;
import java.util.List;

public class ProjectResponseDto{

    private Integer id;
    private Integer issueId;
    private String projectType;
    private String projectDescription;
    private String projectStatus;
    private BigDecimal estimatedCost;
    private BigDecimal actualCost;
    private Date startDate;
    private Date expectedCompletionDate;
    private Date actualCompletionDate;
    private String remarks;
    private List<TenderResponseDto> tenders;

    public Integer getId(){
        return id;
    }

    public void setId(Integer id){
        this.id = issueId;
    }

    public Integer getIssueId(){
        return issueId;
    }

    public void setIssueId(Integer issueId){
        this.issueId = issueId;
    }

    public String getProjectType(){
        return projectType;
    }

    public void setProjectType(String projectType){
        this.projectType = projectType;
    }

    public String getProjectDescription(){
        return projectDescription;
    }

    public void setProjectDescription(String projectDescription){
        this.projectDescription = projectDescription;
    }

    public String getProjectStatus(){
        return projectStatus;
    }

    public void setProjectStatus(String projectStatus){
        this.projectStatus = projectStatus;
    }

    public BigDecimal getEstimatedCost(){
        return estimatedCost;
    }

    public void setEstimatedCost(BigDecimal estimatedCost){
        this.estimatedCost = estimatedCost;
    }

    public BigDecimal getActualCost(){
        return actualCost;
    }

    public void setActualCost(BigDecimal actualCost){
        this.actualCost = actualCost;
    }

    public Date getStartDate(){
        return startDate;
    }

    public void setStartDate(Date startDate){
        this.startDate = startDate;
    }

    public Date getExpectedCompletionDate(){
        return expectedCompletionDate;
    }

    public void setExpectedCompletionDate(Date expectedCompletionDate){
        this.expectedCompletionDate = expectedCompletionDate;
    }

    public Date getActualCompletionDate(){
        return actualCompletionDate;
    }

    public void setActualCompletionDate(Date actualCompletionDate){
        this.actualCompletionDate = actualCompletionDate;
    }

    public String getRemarks(){
        return remarks;
    }

    public void setRemarks(String remarks){
        this.remarks = remarks;
    }

    public List<TenderResponseDto> getTenders(){
        return tenders;
    }

    public void setTenders(List<TenderResponseDto> tenders){
        this.tenders = tenders;
    }
}
