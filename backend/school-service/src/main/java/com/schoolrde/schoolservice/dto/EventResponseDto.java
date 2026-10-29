package com.schoolrde.schoolservice.dto;

import java.sql.Date;

public class EventResponseDto{

	private Integer id;
	private Integer schoolId;
	private String eventType;
	private String detailedDescription;
	private Date eventDate;
	private String location;

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

	public String getEventType(){
	    return eventType;
	}

	public void setEventType(String eventType){
	    this.eventType = eventType;
	}

	public String getDetailedDescription(){
	    return detailedDescription;
	}

	public void setDetailedDescription(String detailedDescription){
	    this.detailedDescription = detailedDescription;
	}

	public Date getEventDate(){
	    return eventDate;
	}

	public void setEventDate(Date eventDate){
	    this.eventDate = eventDate;
	}

	public String getLocation(){
	    return location;
	}

	public void setLocation(String location){
	    this.location = location;
	}

}