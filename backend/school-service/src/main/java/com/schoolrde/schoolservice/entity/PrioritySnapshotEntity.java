package com.schoolrde.schoolservice.entity;

import java.sql.Date;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;


@Entity
@Table(name = "priority_snapshot")
public class PrioritySnapshotEntity{
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;
	
	@Column(name = "school_id", nullable = false)
	private Integer schoolId;

	@Column(name = "snapshot_date", nullable = false)
	private Date snapshotDate;

	@Column(name = "priority_score")
	private Integer priority_score;
	
	@Column(name = "active_issues")
	private Integer activeIssues;
	
	@Column(name = "under_resol_issues")
	private Integer underResolutionIssues;
	
	@Column(name = "resolved_issues")
	private Integer resolvedIssues;
	
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

	public Integer getSchoolId(){
		return schoolId;
	}

	public void setSchoolId(Integer schoolId){
		this.schoolId = schoolId;
	}

	public Date getSnapshotDate(){
		return snapshotDate;
	}

	public void setSnapshotDate(Date snapshotDate){
		this.snapshotDate = snapshotDate;
	}

	public Integer getPriority_score(){
		return priority_score;
	}

	public void setPriority_score(Integer priority_score){
		this.priority_score = priority_score;
	}

	public Integer getActiveIssues(){
		return activeIssues;
	}

	public void setActiveIssues(Integer activeIssues){
		this.activeIssues = activeIssues;
	}

	public Integer getUnderResolutionIssues(){
		return underResolutionIssues;
	}

	public void setUnderResolutionIssues(Integer underResolutionIssues){
		this.underResolutionIssues = underResolutionIssues;
	}

	public Integer getResolvedIssues(){
		return resolvedIssues;
	}

	public void setResolvedIssues(Integer resolvedIssues){
		this.resolvedIssues = resolvedIssues;
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

}
