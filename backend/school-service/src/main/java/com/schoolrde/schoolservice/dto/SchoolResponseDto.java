package com.schoolrde.schoolservice.dto;

import java.math.BigDecimal;
import java.sql.Date;
import java.time.LocalDateTime;

public class SchoolResponseDto{

    private Integer id;
    private String schoolId;
    private String udiseCode;
    private String schoolName;
    private String state;
    private String district;
    private String block;
    private BigDecimal latitude;
    private BigDecimal longitude;
    private String schoolType;
    private String managementType;
    private Date createdOn;
    private String createdBy;
    private Date updatedOn;
    private String updatedBy;

    public SchoolResponseDto(){
    }

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

    public Date getCreatedOn(){
        return createdOn;
    }

    public void setCreatedOn(Date date){
        this.createdOn = date;
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
