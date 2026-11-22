package com.schoolrde.schoolservice.dto;

public class DocumentResponseDto{

	private Integer id;
	private Integer objectId;
	private String objectCategory;
	private SourceResponseDto source;
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

	public void setObjectCategory(String objectCategory){
	    this.objectCategory = objectCategory;
	}

	public SourceResponseDto getSource(){
		return source;
	}

	public void setSource(SourceResponseDto source){
		this.source = source;
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