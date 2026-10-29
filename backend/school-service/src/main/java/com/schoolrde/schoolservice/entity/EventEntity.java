package com.schoolrde.schoolservice.entity;

import java.sql.Date;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;


@Entity
@Table(name = "event")
public class EventEntity{

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;

	
	@Column(name = "school_id", nullable = false)
	private Integer schoolId;
	
	@ManyToOne(fetch = FetchType.LAZY)
	@JoinColumn(name = "event_type_id", nullable = false)
	private EventType eventType;

	@Column(name = "detailed_description", length = 150)
	private String detailedDescription;

	@Column(name = "event_date")
	private Date eventDate;

	@Column(name = "location", length = 50)
	private String location;

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

	public EventType getEventType(){
	    return eventType;
	}

	public void setEventType(EventType eventType){
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