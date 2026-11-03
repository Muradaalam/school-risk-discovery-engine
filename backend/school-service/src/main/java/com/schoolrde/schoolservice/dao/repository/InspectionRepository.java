package com.schoolrde.schoolservice.dao.repository;

import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.InspectionEntity;

public interface InspectionRepository extends JpaRepository<InspectionEntity,Integer>{
	Optional<InspectionEntity> findById(Integer Id);

}
