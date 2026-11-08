package com.schoolrde.schoolservice.dto;

import java.sql.Date;

public class SourceResponseDto{


    private Integer id;
    private String sourceName;
    private String sourceUrl;
    private Date publicationDate;
    
	public Integer getId(){
		return id;
	}

	public void setId(Integer id){
		this.id = id;
	}

	public String getSourceName(){
		return sourceName;
	}

	public void setSourceName(String sourceName){
		this.sourceName = sourceName;
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
