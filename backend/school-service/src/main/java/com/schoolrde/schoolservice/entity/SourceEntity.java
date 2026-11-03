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
@Table(name = "source")
public class SourceEntity{

	@Id
	@GeneratedValue(strategy = GenerationType.IDENTITY)
	private Integer id;
	
	@Column(name = "school_id", nullable = false)
	private Integer schoolId;
	
	@ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "source_name_id", nullable = false)
    private SourceName sourceName;
	
	@Column(name = "source_url", length = 200)
	private String  sourceUrl;
	
	@Column(name = "publication_date")
	private Date publicationDate;
	
    @Column(name = "created_on", insertable = false, updatable = false)
	private Date createdOn;
	
    @Column(name = "created_by", insertable = false, updatable = false)
	private String createdBy;
	
    @Column(name = "updated_on", insertable = false, updatable = false)
	private Date updatedOn;
	
    @Column(name = "updated_by", insertable = false, updatable = false)
	private String updatedBy;

	public Integer getId() {
		return id;
	}

	public void setId(Integer id) {
		this.id = id;
	}

	public Integer getSchoolId() {
		return schoolId;
	}

	public void setSchoolId(Integer schoolId) {
		this.schoolId = schoolId;
	}

	public SourceName getSourceName() {
		return sourceName;
	}

	public void setSourceName(SourceName sourceName) {
		this.sourceName = sourceName;
	}

	public String getSourceUrl() {
		return sourceUrl;
	}

	public void setSourceUrl(String sourceUrl) {
		this.sourceUrl = sourceUrl;
	}

	public Date getPublicationDate() {
		return publicationDate;
	}

	public void setPublicationDate(Date publicationDate) {
		this.publicationDate = publicationDate;
	}

	public Date getCreatedOn() {
		return createdOn;
	}

	public void setCreatedOn(Date createdOn) {
		this.createdOn = createdOn;
	}

	public String getCreatedBy() {
		return createdBy;
	}

	public void setCreatedBy(String createdBy) {
		this.createdBy = createdBy;
	}

	public Date getUpdatedOn() {
		return updatedOn;
	}

	public void setUpdatedOn(Date updatedOn) {
		this.updatedOn = updatedOn;
	}

	public String getUpdatedBy() {
		return updatedBy;
	}

	public void setUpdatedBy(String updatedBy) {
		this.updatedBy = updatedBy;
	}
}

