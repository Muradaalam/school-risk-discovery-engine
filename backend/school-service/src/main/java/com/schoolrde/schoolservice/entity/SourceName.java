package com.schoolrde.schoolservice.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "source_name")
public class SourceName{
	
	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;
	
	@Column(name = "source_name", nullable = false, length = 30, unique = true)
	private String source_name;

	@Column(name = "description", length = 100)
	private String description;

	public Integer getId(){
		return id;
	}

	public void setId(Integer id){
		this.id = id;
	}

	public String getSource_name(){
		return source_name;
	}

	public void setSource_name(String source_name){
		this.source_name = source_name;
	}

	public String getDescription(){
		return description;
	}

	public void setDescription(String description){
		this.description = description;
	}

}
