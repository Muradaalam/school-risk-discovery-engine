package com.schoolrde.schoolservice.entity;

import java.sql.Date;
import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

@Entity
@Table(name = "issue")
public class IssueEntity{

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;
	
	@Column(name = "school_id", nullable = false)
	private Integer schoolId;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "issue_type_id", referencedColumnName = "id", insertable = false, updatable = false)
	private IssueType issueType;
	
	@Column(name = "status_id",  nullable = false)
	private Integer statusId;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "status_id", referencedColumnName = "id", insertable = false, updatable = false)
	private IssueStatus issueStatus;

	@Column(name = "first_detected")
	private Date firstDetected;
	
	@Column(name = "last_updated")
	private Date lastUpdated;
	
	@Column(name = "resolved_at")
	private Date resolvedAt;
	
	@Column(name = "created_on", insertable = false, updatable = false)
	private Date createdOn;
	
	@Column(name = "created_by", insertable = false, updatable = false)
	private String createdBy;
	
	@Column(name = "updated_on", insertable = false, updatable = false)
	private Date updatedOn;
	
	@Column(name = "updated_by", insertable = false, updatable = false)
	private String updatedBy;
	
    @OneToMany(fetch = FetchType.LAZY)
    @JoinColumn(name = "issue_id", referencedColumnName = "id", insertable = false, updatable = false)
    private List<ProjectEntity> projects;

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

    public Integer getStatusId(){
        return statusId;
    }
    
    public IssueType getIssueType(){
        return issueType;
    }

    public void setIssueType(IssueType issueType){
        this.issueType = issueType;
    }

    public void setStatusId(Integer statusId){
        this.statusId = statusId;
    }

    public IssueStatus getIssueStatus(){
        return issueStatus;
    }

    public void setIssueStatus(IssueStatus issueStatus){
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

    public Date getCreatedOn(){
        return createdOn;
    }

    public void setCreatedOn(Date createdOn){
        this.createdOn = createdOn;
    }

    public String getCreatedBy(){
        return createdBy;
    }

    public void setCreatedBy(String createdBy){
        this.createdBy = createdBy;
    }

    public Date getUpdatedOn(){
        return updatedOn;
    }

    public void setUpdatedOn(Date updatedOn){
        this.updatedOn = updatedOn;
    }

    public String getUpdatedBy(){
        return updatedBy;
    }

    public void setUpdatedBy(String updatedBy){
        this.updatedBy = updatedBy;
    }
    
	public List<ProjectEntity> getProjects(){
		return projects;
	}

	public void setProjects(List<ProjectEntity> projects){
		this.projects = projects;
	}

}