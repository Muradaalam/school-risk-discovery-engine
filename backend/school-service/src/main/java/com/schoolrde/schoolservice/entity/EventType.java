package com.schoolrde.schoolservice.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "event_type")
public class EventType{

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	@Column(name = "id", nullable = false)
	private Integer id;

	@Column(name = "event_type", nullable = false, unique = true, length = 30)
	private String eventType;

	@Column(name = "description", length = 100)
	private String description;

	public Integer getId(){
	    return id;
	}

	public void setId(Integer id){
	    this.id = id;
	}

	public String getEventType(){
	    return eventType;
	}

	public void setEventType(String eventType){
	    this.eventType = eventType;
	}

	public String getDescription(){
	    return description;
	}

	public void setDescription(String description){
	    this.description = description;
	}
}
