package com.schoolrde.schoolservice.entity;

import java.sql.Date;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;


@Entity
@Table(name = "inspection")
public class InspectionEntity{

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;
	
	@Column(name = "school_id", nullable = false)
	private Integer schoolId;
	
	@Column(name = "inspection_date", nullable = false)
	private Date inspectionDate;
	
	@Column(name = "inspection_type", length = 50)
	private String inspectionType;
	
	@Column(name = "remarks", length = 100)
	private String remarks;
	
	@Column(name = "inspector_name", length = 50)
	private String inspectorName;
	
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

	public Date getInspectionDate(){
		return inspectionDate;
	}

	public void setInspectionDate(Date inspectionDate){
		this.inspectionDate = inspectionDate;
	}

	public String getInspectionType(){
		return inspectionType;
	}

	public void setInspectionType(String inspectionType){
		this.inspectionType = inspectionType;
	}

	public String getRemarks(){
		return remarks;
	}

	public void setRemarks(String remarks){
		this.remarks = remarks;
	}

	public String getInspectorName(){
		return inspectorName;
	}

	public void setInspectorName(String inspectorName){
		this.inspectorName = inspectorName;
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
