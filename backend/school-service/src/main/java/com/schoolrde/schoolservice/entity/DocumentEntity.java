package com.schoolrde.schoolservice.entity;

import java.sql.Date;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "document")
public class DocumentEntity {

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;
	
	@Column(name = "object_id", nullable = false)
	private Integer objectId;
	
	@Column(name = "object_category_id", nullable = false)
	private Integer objectCategoryId;
	
	@Column(name = "source_id")
	private Integer sourceId;
	
	@Column(name = "document_name", nullable = false, length = 50)
	private String documentName;
	
	@Column(name = "doc_path", length = 100)
	private String docPath;
	
	@Column(name = "description", length = 150)
	private String description;
	
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

	public Integer getObjectId(){
		return objectId;
	}

	public void setObjectId(Integer objectId){
		this.objectId = objectId;
	}

	public Integer getObjectCategoryId(){
		return objectCategoryId;
	}

	public void setObjectCategoryId(Integer objectCategoryId){
		this.objectCategoryId = objectCategoryId;
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

	public Date getCreatedOn(){
		return createdOn;
	}

	public void setCreatedOn(Date createdOn){
		this.createdOn = createdOn;
	}

	public String getCreatedBy(){
		return createdBy;
	}

	public void setCreatedBy(String createdBy){
		this.createdBy = createdBy;
	}

	public Date getUpdatedOn(){
		return updatedOn;
	}

	public void setUpdatedOn(Date updatedOn){
		this.updatedOn = updatedOn;
	}

	public String getUpdatedBy(){
		return updatedBy;
	}

	public void setUpdatedBy(String updatedBy){
		this.updatedBy = updatedBy;
	}
	
}


