package com.schoolrde.schoolservice.entity;
import jakarta.persistence.*;
import java.sql.Date;
import java.math.BigDecimal;

@Entity
@Table(name = "tender")
public class TenderEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "project_id", nullable = false)
    private Integer projectId;

    @Column(name = "tender_number", nullable = false, unique = true, length = 30)
    private String tenderNumber;

    @Column(name = "tender_title", nullable = false, length = 100)
    private String tenderTitle;

    @Column(name = "tender_description", length = 100)
    private String tenderDescription;

    @Column(name = "tender_status_id", nullable = false)
    private Integer tenderStatusId;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "tender_status_id", referencedColumnName = "id", insertable = false, updatable = false)
    private TenderStatus tenderStatus;

    @Column(name = "estimated_amount", precision = 10, scale = 2)
    private BigDecimal estimatedAmount;

    @Column(name = "awarded_amount", precision = 10, scale = 2)
    private BigDecimal awardedAmount;

    @Column(name = "publication_date")
    private Date publicationDate;

    @Column(name = "submission_deadline")
    private Date submissionDeadline;

    @Column(name = "award_date")
    private Date awardDate;

    @Column(name = "contractor_name", length = 50)
    private String contractorName;

    @Column(name = "contract_start_date")
    private Date contractStartDate;

    @Column(name = "contract_end_date")
    private Date contractEndDate;

    @Column(name = "created_on", insertable = false, updatable = false)
    private Date createdOn;

    @Column(name = "created_by", insertable = false, updatable = false)
    private String createdBy;

    @Column(name = "updated_on", insertable = false, updatable = false)
    private Date updatedOn;

    @Column(name = "updated_by", insertable = false, updatable = false)
    private String updatedBy;

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

    public Integer getTenderStatusId(){
        return tenderStatusId;
    }

    public void setTenderStatusId(Integer tenderStatusId){
        this.tenderStatusId = tenderStatusId;
    }

    public TenderStatus getTenderStatus(){
        return tenderStatus;
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

    public void setContractEndDate(Date contractEndDate){
        this.contractEndDate = contractEndDate;
    }

    public Date getCreatedOn(){
        return createdOn;
    }

    public String getCreatedBy(){
        return createdBy;
    }

    public Date getUpdatedOn(){
        return updatedOn;
    }

    public String getUpdatedBy(){
        return updatedBy;
    }
}
