package com.schoolrde.schoolservice.dto;

import java.math.BigDecimal;
import java.util.List;

public class SchoolEntireResponseDto{

    private Integer id;
    private String schoolId;
    private String udiseCode;
    private String schoolName;
    private String state;
    private String district;
    private String block;
    private BigDecimal latitude;
    private BigDecimal longitude;
    private String schoolType;
    private String managementType;
    private List<PrioritySnapshotResponseDto> prioritySnapshots;
    private List<IssueResponseDto> issues;
    private List<InspectionResponseDto> inspections;
    private List<SourceResponseDto> sources;
    private List<EventResponseDto> events;
    
	public Integer getId(){
		return id;
	}

	public void setId(Integer id){
		this.id = id;
	}

	public String getSchoolId(){
		return schoolId;
	}

	public void setSchoolId(String schoolId){
		this.schoolId = schoolId;
	}

	public String getUdiseCode(){
		return udiseCode;
	}

	public void setUdiseCode(String udiseCode){
		this.udiseCode = udiseCode;
	}

	public String getSchoolName(){
		return schoolName;
	}

	public void setSchoolName(String schoolName){
		this.schoolName = schoolName;
	}

	public String getState(){
		return state;
	}

	public void setState(String state){
		this.state = state;
	}

	public String getDistrict(){
		return district;
	}

	public void setDistrict(String district){
		this.district = district;
	}

	public String getBlock(){
		return block;
	}

	public void setBlock(String block){
		this.block = block;
	}

	public BigDecimal getLatitude(){
		return latitude;
	}

	public void setLatitude(BigDecimal latitude){
		this.latitude = latitude;
	}

	public BigDecimal getLongitude(){
		return longitude;
	}

	public void setLongitude(BigDecimal longitude){
		this.longitude = longitude;
	}

	public String getSchoolType(){
		return schoolType;
	}

	public void setSchoolType(String schoolType){
		this.schoolType = schoolType;
	}

	public String getManagementType(){
		return managementType;
	}

	public void setManagementType(String managementType){
		this.managementType = managementType;
	}

	public List<PrioritySnapshotResponseDto> getPrioritySnapshots(){
		return prioritySnapshots;
	}

	public void setPrioritySnapshots(List<PrioritySnapshotResponseDto> prioritySnapshots){
		this.prioritySnapshots = prioritySnapshots;
	}

	public List<IssueResponseDto> getIssues(){
		return issues;
	}

	public void setIssues(List<IssueResponseDto> issues){
		this.issues = issues;
	}

	public List<InspectionResponseDto> getInspections(){
		return inspections;
	}

	public void setInspections(List<InspectionResponseDto> inspections){
		this.inspections = inspections;
	}

	public List<SourceResponseDto> getSources(){
		return sources;
	}

	public void setSources(List<SourceResponseDto> sources){
		this.sources = sources;
	}

	public List<EventResponseDto> getEvents(){
		return events;
	}

	public void setEvents(List<EventResponseDto> events){
		this.events = events;
	}

}
