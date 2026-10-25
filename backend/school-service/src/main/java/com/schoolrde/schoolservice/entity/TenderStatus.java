package com.schoolrde.schoolservice.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "tender_status")
public class TenderStatus{

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer id;

    @Column(name = "status", nullable = false, unique = true, length = 30)
    private String status;

    @Column(name = "description", length = 100)
    private String description;

    public Integer getId(){
        return id;
    }

    public void setId(Integer id){
        this.id = id;
    }

    public String getStatus(){
        return status;
    }

    public void setStatus(String status){
        this.status = status;
    }

    public String getDescription(){
        return description;
    }

    public void setDescription(String description){
        this.description = description;
    }
}
