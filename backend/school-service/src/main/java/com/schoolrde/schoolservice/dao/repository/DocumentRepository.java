package com.schoolrde.schoolservice.dao.repository;

import java.util.List;
import java.util.Optional;

import org.springframework.data.jpa.repository.JpaRepository;

import com.schoolrde.schoolservice.entity.DocumentEntity;

public interface DocumentRepository extends JpaRepository<DocumentEntity,Integer>{
	Optional<DocumentEntity> findById(Integer Id);
	
	List<DocumentEntity> findByObjectIdAndObjectCategoryId(Integer objectId, Integer objectCategoryId);

	List<DocumentEntity> findBySourceId(Integer sourceId);

}