package com.schoolrde.schoolservice.entity;

import jakarta.persistence.*;
import java.math.BigDecimal;
import java.sql.Date;
import java.util.List;

@Entity
@Table(name = "project")
public class ProjectEntity{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "issue_id")
    private Integer issueId;

    @Column(name = "project_type", nullable = false)
    private String projectType = "NEW";

    @Column(name = "project_description")
    private String projectDescription;

    @Column(name = "project_status", nullable = false)
    private String projectStatus = "PENDING";

    @Column(name = "estimated_cost", precision = 10, scale = 2)
    private BigDecimal estimatedCost;

    @Column(name = "actual_cost", precision = 10, scale = 2)
    private BigDecimal actualCost;

    @Column(name = "start_date")
    private Date startDate;

    @Column(name = "expected_completion_date")
    private Date expectedCompletionDate;

    @Column(name = "actual_completion_date")
    private Date actualCompletionDate;

    @Column(name = "remarks")
    private String remarks;

    @Column(name = "created_on", insertable = false, updatable = false)
    private Date createdOn;

    @Column(name = "created_by", insertable = false, updatable = false)
    private String createdBy;

    @Column(name = "updated_on", insertable = false, updatable = false)
    private Date updatedOn;

    @Column(name = "updated_by", insertable = false, updatable = false)
    private String updatedBy;
    
    @OneToMany(fetch = FetchType.LAZY)
    @JoinColumn(name = "project_id", referencedColumnName = "id", insertable = false, updatable = false)
    private List<TenderEntity> tenders;

    public Integer getId(){
        return id;
    }

    public void setId(Integer id){
        this.id = id;
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
    
	public List<TenderEntity> getTenders(){
		return tenders;
	}

	public void setTenders(List<TenderEntity> tenders){
		this.tenders = tenders;
	}

}

