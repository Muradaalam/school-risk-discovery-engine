package com.schoolrde.schoolservice.dao.bussiness;

import java.util.Optional;

import com.schoolrde.schoolservice.entity.EventEntity;

public interface EventDao{
    Optional<EventEntity> findById(Integer id);
 
}