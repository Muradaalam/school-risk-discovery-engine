package com.schoolrde.schoolservice.dto;

import java.math.BigDecimal;
import java.sql.Date;

public class TenderResponseDto{

    private Integer id;
    private Integer projectId;
    private String tenderNumber;
    private String tenderTitle;
    private String tenderDescription;
    private String tenderStatus;
    private BigDecimal estimatedAmount;
    private BigDecimal awardedAmount;
    private Date publicationDate;
    private Date submissionDeadline;
    private Date awardDate;
    private String contractorName;
    private Date contractStartDate;
    private Date contractEndDate;

    public Integer getId(){
        return id;
    }

    public void setId(Integer id){
        this.id = id;
    }

 
    public Integer getProjectId(){
        return projectId;
    }

    public void setProjectId(Integer projectId){
        this.projectId = projectId;
    }

    public String getTenderNumber(){
        return tenderNumber;
    }

    public void setTenderNumber(String tenderNumber){
        this.tenderNumber = tenderNumber;
    }

    public String getTenderTitle(){
        return tenderTitle;
    }

    public void setTenderTitle(String tenderTitle){
        this.tenderTitle = tenderTitle;
    }

    public String getTenderDescription(){
        return tenderDescription;
    }

    public void setTenderDescription(String tenderDescription){
        this.tenderDescription = tenderDescription;
    }

    public String getTenderStatus(){
        return tenderStatus;
    }

    public void setTenderStatus(String tenderStatus){
        this.tenderStatus = tenderStatus;
    }

    public BigDecimal getEstimatedAmount(){
        return estimatedAmount;
    }

    public void setEstimatedAmount(BigDecimal estimatedAmount){
        this.estimatedAmount = estimatedAmount;
    }

    public BigDecimal getAwardedAmount(){
        return awardedAmount;
    }

    public void setAwardedAmount(BigDecimal awardedAmount){
        this.awardedAmount = awardedAmount;
    }

    public Date getPublicationDate(){
        return publicationDate;
    }

    public void setPublicationDate(Date publicationDate){
        this.publicationDate = publicationDate;
    }

    public Date getSubmissionDeadline(){
        return submissionDeadline;
    }

    public void setSubmissionDeadline(Date submissionDeadline){
        this.submissionDeadline = submissionDeadline;
    }

    public Date getAwardDate(){
        return awardDate;
    }

    public void setAwardDate(Date awardDate){
        this.awardDate = awardDate;
    }

    public String getContractorName(){
        return contractorName;
    }

    public void setContractorName(String contractorName){
        this.contractorName = contractorName;
    }

    public Date getContractStartDate(){
        return contractStartDate;
    }

    public void setContractStartDate(Date contractStartDate){
        this.contractStartDate = contractStartDate;
    }

    public Date getContractEndDate(){
        return contractEndDate;
    }

    public void setContractEndDate(Date date){
        this.contractEndDate = date;
    }

	
}
