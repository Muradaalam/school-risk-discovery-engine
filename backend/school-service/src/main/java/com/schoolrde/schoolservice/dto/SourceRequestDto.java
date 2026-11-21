package com.schoolrde.schoolservice.dto;

import java.sql.Date;

public class SourceRequestDto{

	private Integer id;
	private Integer schoolId;
	private Integer sourceNameId;
	private String sourceUrl;
	private Date publicationDate;

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

	public Integer getSourceNameId(){
	    return sourceNameId;
	}

	public void setSourceNameId(Integer sourceNameId){
	    this.sourceNameId = sourceNameId;
	}

	public String getSourceUrl(){
	    return sourceUrl;
	}

	public void setSourceUrl(String sourceUrl){
	    this.sourceUrl = sourceUrl;
	}

	public Date getPublicationDate(){
	    return publicationDate;
	}

	public void setPublicationDate(Date publicationDate){
	    this.publicationDate = publicationDate;
	}

}