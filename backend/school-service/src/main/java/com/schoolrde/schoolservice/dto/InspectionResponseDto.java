package com.schoolrde.schoolservice.dto;

import java.sql.Date;

public class InspectionResponseDto{

    private Integer id;
    private Date inspectionDate;
    private String inspectionType;
    private String remarks;
    private String inspectorName;
    
	public Integer getId(){
		return id;
	}

	public void setId(Integer id){
		this.id = id;
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
	
}