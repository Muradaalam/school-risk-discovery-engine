package com.schoolrde.schoolservice.dto;


public class DocumentRequestDto{

	private Integer id;
	private Integer objectId;
	private String objectCategory;
	private Integer sourceId;
	private String documentName;
	private String docPath;
	private String description;
	
	// Getters and setters are generated using STS: Source > Generate Getters and Setters
	public Integer getId(){
	    return id;
	}

	public void setId(Integer id){
	    this.id = id;
	}

	public Integer getObjectId(){
	    return objectId;
	}

	public void setObjectId(Integer objectId){
	    this.objectId = objectId;
	}

	public String getObjectCategory(){
	    return objectCategory;
	}

	public void setObjectCategoryId(String objectCategory){
	    this.objectCategory = objectCategory;
	}

	public Integer getSourceId(){
	    return sourceId;
	}

	public void setSourceId(Integer sourceId){
	    this.sourceId = sourceId;
	}

	public String getDocumentName(){
	    return documentName;
	}

	public void setDocumentName(String documentName){
	    this.documentName = documentName;
	}

	public String getDocPath(){
	    return docPath;
	}

	public void setDocPath(String docPath){
	    this.docPath = docPath;
	}

	public String getDescription(){
	    return description;
	}

	public void setDescription(String description){
	    this.description = description;
	}

}