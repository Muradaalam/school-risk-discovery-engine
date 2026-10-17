package com.schoolrde.schoolservice.entity;

import java.math.BigDecimal;
import java.util.List;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.JoinColumn;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

@Entity
@Table(name = "school")
public class SchoolWithIssueEntity{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "school_id", nullable = false, unique = true, length = 50)
    private String schoolId;

    @Column(name = "udise_code", length = 20)
    private String udiseCode;

    @Column(name = "school_name", nullable = false, length = 100)
    private String schoolName;

    @Column(name = "state", length = 30)
    private String state;

    @Column(name = "district", length = 50)
    private String district;

    @Column(name = "block", length = 50)
    private String block;

    @Column(name = "latitude", precision = 10, scale = 7)
    private BigDecimal latitude;

    @Column(name = "longitude", precision = 10, scale = 7)
    private BigDecimal longitude;

    @Column(name = "school_type", length = 50)
    private String schoolType;

    @Column(name = "management_type", length = 50)
    private String managementType;

    @OneToMany(fetch = FetchType.LAZY)
    @JoinColumn(name = "school_id", referencedColumnName = "id", insertable = false, updatable = false)
    private List<IssueEntity> issues;

    public Integer getId(){
        return id;
    }

    public void setId(Integer id){
        this.id = id;
    }

    public String getSchoolId(){
        return schoolId;
    }

    public void setSchoolId(String schoolId){
        this.schoolId = schoolId;
    }

    public String getUdiseCode(){
        return udiseCode;
    }

    public void setUdiseCode(String udiseCode){
        this.udiseCode = udiseCode;
    }

    public String getSchoolName(){
        return schoolName;
    }

    public void setSchoolName(String schoolName){
        this.schoolName = schoolName;
    }

    public String getState(){
        return state;
    }

    public void setState(String state){
        this.state = state;
    }

    public String getDistrict(){
        return district;
    }

    public void setDistrict(String district){
        this.district = district;
    }

    public String getBlock(){
        return block;
    }

    public void setBlock(String block){
        this.block = block;
    }

    public BigDecimal getLatitude(){
        return latitude;
    }

    public void setLatitude(BigDecimal latitude){
        this.latitude = latitude;
    }

    public BigDecimal getLongitude(){
        return longitude;
    }

    public void setLongitude(BigDecimal longitude){
        this.longitude = longitude;
    }

    public String getSchoolType(){
        return schoolType;
    }

    public void setSchoolType(String schoolType){
        this.schoolType = schoolType;
    }

    public String getManagementType(){
        return managementType;
    }

    public void setManagementType(String managementType){
        this.managementType = managementType;
    }

    public List<IssueEntity> getIssues(){
        return issues;
    }

    public void setIssues(List<IssueEntity> issues){
        this.issues = issues;
    }
}




