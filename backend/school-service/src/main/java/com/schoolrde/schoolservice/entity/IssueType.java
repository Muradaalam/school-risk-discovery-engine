package com.schoolrde.schoolservice.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;


@Entity
@Table(name = "issue_type")
public class IssueType{

	@Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id; 
	
	@Column(name = "issue_type", nullable = false, length = 30, unique = true)
	private String issueType;

	@Column(name = "description", length = 100)
	private String description;

    public Integer getId(){
        return id;
    }

    public void setId(Integer id){
        this.id = id;
    }

    public String getIssue_type(){
        return issueType;
    }

    public void setIssueType(String issueType){
        this.issueType = issueType;
    }

    public String getDescription(){
        return description;
    }

    public void setDescription(String description){
        this.description = description;
    }
}