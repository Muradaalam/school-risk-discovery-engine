package com.schoolrde.schoolservice.entity;

import java.sql.Date;
import java.util.List;
import java.util.Optional;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.OneToOne;
import jakarta.persistence.Table;

@Entity
@Table(name = "issue")
public class IssueEntity{

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;
	
	@Column(name = "school_id", nullable = false)
	private Integer school_id;
	
	@Column(name = "issue_type_id", nullable = false)
	private Integer issue_type_id;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "issue_type_id", referencedColumnName = "id", insertable = false, updatable = false)
	private IssueType issueType;
	
	@Column(name = "status_id",  nullable = false)
	private Integer status_id;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "status_id", referencedColumnName = "id", insertable = false, updatable = false)
	private IssueStatus issueStatus;

	@Column(name = "first_detected")
	private Date first_detected;
	
	@Column(name = "last_updated")
	private Date last_updated;
	
	@Column(name = "resolved_at")
	private Date resolved_at;
	
	@Column(name = "created_on", insertable = false, updatable = false)
	private Date created_on;
	
	@Column(name = "created_by", insertable = false, updatable = false)
	private String created_by;
	
	@Column(name = "updated_on", insertable = false, updatable = false)
	private Date updated_on;
	
	@Column(name = "updated_by", insertable = false, updatable = false)
	private String updated_by;
	
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
        return school_id;
    }

    public void setSchoolId(Integer school_id){
        this.school_id = school_id;
    }

    public Integer getIssueTypeId(){
        return issue_type_id;
    }

    public void setIssueTypeId(Integer issue_type_id){
        this.issue_type_id = issue_type_id;
    }

    public Integer getStatusId(){
        return status_id;
    }
    
    public IssueType getIssueType() {
        return issueType;
    }

    public void setIssueType(IssueType issueType) {
        this.issueType = issueType;
    }

    public void setStatusId(Integer status_id){
        this.status_id = status_id;
    }

    public IssueStatus getIssueStatus() {
        return issueStatus;
    }

    public void setIssueStatus(IssueStatus issueStatus) {
        this.issueStatus = issueStatus;
    }
    
    public Date getFirstDetected(){
        return first_detected;
    }

    public void setFirstDetected(Date first_detected){
        this.first_detected = first_detected;
    }

    public Date getLastUpdated(){
        return last_updated;
    }

    public void setLastUpdated(Date last_updated){
        this.last_updated = last_updated;
    }

    public Date getResolvedAt(){
        return resolved_at;
    }

    public void setResolvedAt(Date resolved_at){
        this.resolved_at = resolved_at;
    }

    public Date getCreatedOn(){
        return created_on;
    }

    public void setCreatedOn(Date created_on){
        this.created_on = created_on;
    }

    public String getCreatedBy(){
        return created_by;
    }

    public void setCreatedBy(String created_by){
        this.created_by = created_by;
    }

    public Date getUpdatedOn(){
        return updated_on;
    }

    public void setUpdatedOn(Date updated_on){
        this.updated_on = updated_on;
    }

    public String getUpdatedBy(){
        return updated_by;
    }

    public void setUpdatedBy(String updated_by){
        this.updated_by = updated_by;
    }

	public List<ProjectEntity> getProjects(){
		return projects;
	}

	public void setProjects(List<ProjectEntity> projects){
		this.projects = projects;
	}
}




